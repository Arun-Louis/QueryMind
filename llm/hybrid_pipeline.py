from langchain_groq import ChatGroq
from langchain_community.utilities import SQLDatabase
from langchain_classic.chains import create_sql_query_chain
from langchain_community.chat_message_histories import ChatMessageHistory
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from pathlib import Path
from db.connect import get_vector_connection
import os

load_dotenv(Path(__file__).parent.parent / ".env")

# ── LLM setup ──────────────────────────────────────────────────────
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY")
)

# ── SQL setup ──────────────────────────────────────────────────────
db = SQLDatabase.from_uri(
    f"postgresql+psycopg2://{os.getenv('VECTOR_DB_USER')}:{os.getenv('VECTOR_DB_PASSWORD')}@{os.getenv('VECTOR_DB_HOST')}:{os.getenv('VECTOR_DB_PORT')}/{os.getenv('VECTOR_DB_NAME')}",
    sample_rows_in_table_info=2,
    custom_table_info={
        "category_translation": "Maps Portuguese category names to English. "
                                 "product_category_name is Portuguese. "
                                 "product_category_name_english is English. "
                                 "Join with products.product_category_name to get English names."
    }
)
sql_chain = create_sql_query_chain(llm, db)

# ── Embedding setup ────────────────────────────────────────────────
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# ── Conversation memory ────────────────────────────────────────────
history = ChatMessageHistory()


# ── Step 1: Router ─────────────────────────────────────────────────
def classify_question(question):
    prompt = f"""Classify this question into exactly one category:
- SQL: needs numbers, counts, rankings, or aggregations from a database
- RAG: needs qualitative context, explanations, or strategy from documents
- HYBRID: needs both database numbers AND document context

Question: {question}

Reply with only one word: SQL, RAG, or HYBRID."""

    response = llm.invoke(prompt)
    classification = response.content.strip().upper()

    if "HYBRID" in classification:
        return "HYBRID"
    elif "RAG" in classification:
        return "RAG"
    else:
        return "SQL"


# ── Step 2: SQL path ───────────────────────────────────────────────
def extract_sql(raw):
    if "```sql" in raw:
        return raw.split("```sql")[-1].split("```")[0].strip()
    if "SQLQuery:" in raw:
        return raw.split("SQLQuery:")[-1].strip()
    if "SELECT" in raw.upper() or "WITH" in raw.upper():
        lines = raw.split("\n")
        sql_lines = []
        collecting = False
        for line in lines:
            if line.strip().upper().startswith(("SELECT", "WITH")):
                collecting = True
            if collecting:
                sql_lines.append(line)
                if line.strip().endswith(";"):
                    break
        return "\n".join(sql_lines).strip()
    return raw.strip()

def run_sql(question):
    try:
        raw = sql_chain.invoke({"question": question})
        clean_sql = extract_sql(raw)
        result = db.run(clean_sql)
        return clean_sql, str(result)
    except Exception as e:
        return None, f"SQL error: {e}"


# ── Step 3: RAG path ───────────────────────────────────────────────
def run_rag(question, top_k=3):
    question_embedding = embedding_model.encode(question).tolist()

    conn = get_vector_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT filename, content, 1 - (embedding <=> %s::vector) AS similarity
        FROM document_chunks
        ORDER BY embedding <=> %s::vector
        LIMIT %s;
    """, (question_embedding, question_embedding, top_k))

    results = cursor.fetchall()
    cursor.close()
    conn.close()

    context = ""
    sources = []
    for filename, content, similarity in results:
        context += f"\n[Source: {filename}]\n{content}\n"
        sources.append(filename)

    return context, sources


# ── Step 4: Synthesizer ────────────────────────────────────────────
def synthesize_answer(question, sql_result=None, rag_context=None, sql_query=None):
    prompt = f"Question: {question}\n\n"

    if sql_result:
        prompt += f"Database results:\n{sql_result}\n\n"

    if rag_context:
        prompt += f"Relevant document context:\n{rag_context}\n\n"

    prompt += "Based on the above information, provide a clear and concise answer. If both data and context are available, combine them into one coherent response."

    response = llm.invoke(prompt)
    return response.content.strip()


# ── Step 5: Main pipeline ──────────────────────────────────────────
def ask(question):
    print(f"\n{'='*60}")
    print(f"Question: {question}")

    history_text = ""
    if history.messages:
        history_text = "Previous conversation:\n"
        for msg in history.messages[-4:]:
            role = "User" if msg.type == "human" else "Assistant"
            history_text += f"{role}: {msg.content}\n"
        history_text += "\n"

    full_question = f"{history_text}Current question: {question}" if history_text else question

    classification = classify_question(full_question)
    print(f"Classification: {classification}")

    sql_query = None
    sql_result = None
    rag_context = None
    sources = []

    if classification in ["SQL", "HYBRID"]:
        sql_query, sql_result = run_sql(full_question)
        print(f"SQL executed: {'yes' if sql_query else 'failed'}")

    if classification in ["RAG", "HYBRID"]:
        rag_context, sources = run_rag(question)
        print(f"RAG chunks retrieved: {len(sources)}")

    answer = synthesize_answer(question, sql_result, rag_context, sql_query)

    print(f"\nAnswer:\n{answer}")

    if sql_query:
        print(f"\nSQL used:\n{sql_query}")
    if sources:
        print(f"\nSources: {', '.join(set(sources))}")

    history.add_user_message(question)
    history.add_ai_message(answer)

    return answer


# ── Test it ────────────────────────────────────────────────────────
if __name__ == "__main__":
    ask("How many orders were placed in November 2017?")
    ask("Why did sales grow so much in November 2017?")
    ask("What were the top 3 product categories and what drove their performance?")