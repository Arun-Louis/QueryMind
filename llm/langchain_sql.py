from langchain_groq import ChatGroq
from langchain_community.utilities import SQLDatabase
from langchain_classic.chains import create_sql_query_chain
from langchain_community.chat_message_histories import ChatMessageHistory
from dotenv import load_dotenv
import os

load_dotenv()

db = SQLDatabase.from_uri(
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}",
    sample_rows_in_table_info=2,
    custom_table_info={
        "category_translation": "Maps Portuguese category names to English. "
                                 "Column product_category_name is Portuguese. "
                                 "Column product_category_name_english is English. "
                                 "The products table only has product_category_name (Portuguese). "
                                 "To get English names join products.product_category_name = category_translation.product_category_name.",
    }
)

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY")
)

chain = create_sql_query_chain(llm, db)

history = ChatMessageHistory()

def extract_sql(raw):
    if "```sql" in raw:
        return raw.split("```sql")[-1].split("```")[0].strip()
    if "SQLQuery:" in raw:
        return raw.split("SQLQuery:")[-1].strip()
    if "SELECT" in raw.upper():
        lines = raw.split("\n")
        sql_lines = []
        collecting = False
        for line in lines:
            if line.strip().upper().startswith("SELECT") or line.strip().upper().startswith("WITH"):
                collecting = True
            if collecting:
                sql_lines.append(line)
                if line.strip().endswith(";"):
                    break
        return "\n".join(sql_lines).strip()
    return raw.strip()

def ask(question):
    print(f"\nYou: {question}")

    history_text = ""
    if history.messages:
        history_text = "Previous conversation:\n"
        for msg in history.messages:
            role = "User" if msg.type == "human" else "Assistant"
            history_text += f"{role}: {msg.content}\n"
        history_text += "\n"

    full_question = f"{history_text}Current question: {question}"

    sql = chain.invoke({"question": full_question})
    clean_sql = extract_sql(sql)

    print(f"SQL: {clean_sql}")

    try:
        result = db.run(clean_sql)
        print(f"Result: {result}")
        history.add_user_message(question)
        history.add_ai_message(str(result))
        return result
    except Exception as e:
        print(f"SQL failed: {e}")
        return None

ask("What are the top 3 product categories by number of orders? Use orders, order_items, and products tables only.")
ask("What is the average payment value for orders in cama_mesa_banho, beleza_saude, and esporte_lazer? Use orders, order_items, products, and order_payments tables only. Filter using product_category_name directly on the products table.")