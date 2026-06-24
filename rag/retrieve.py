from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from db.connect import get_vector_connection

load_dotenv()

model = SentenceTransformer("all-MiniLM-L6-v2")

def retrieve_relevant_chunks(question, top_k=3):
    """
    Given a question, find the most semantically similar document chunks.
    
    How it works:
    1. Embed the question into a 384-dim vector
    2. Use pgvector's <=> operator (cosine distance) to find closest chunks
    3. Return top_k most relevant chunks
    """
    # Embed the question
    question_embedding = model.encode(question).tolist()

    conn = get_vector_connection()
    cursor = conn.cursor()

    # The <=> operator is pgvector's cosine distance
    # ORDER BY distance ASC means most similar first
    cursor.execute("""
        SELECT filename, content, 1 - (embedding <=> %s::vector) AS similarity
        FROM document_chunks
        ORDER BY embedding <=> %s::vector
        LIMIT %s;
    """, (question_embedding, question_embedding, top_k))

    results = cursor.fetchall()
    cursor.close()
    conn.close()

    return results

if __name__ == "__main__":
    questions = [
        "Why did sales grow in November 2017?",
        "What were the top product categories?",
        "What delivery problems did Olist face?"
    ]

    for question in questions:
        print(f"\nQuestion: {question}")
        print("-" * 50)
        chunks = retrieve_relevant_chunks(question, top_k=2)
        for filename, content, similarity in chunks:
            print(f"Source: {filename} | Similarity: {similarity:.3f}")
            print(f"Content: {content[:200]}...")
            print()