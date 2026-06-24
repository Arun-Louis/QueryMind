import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

def get_connection():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    return conn

def get_vector_connection():
    conn = psycopg2.connect(
        host=os.getenv("VECTOR_DB_HOST"),
        port=os.getenv("VECTOR_DB_PORT"),
        dbname=os.getenv("VECTOR_DB_NAME"),
        user=os.getenv("VECTOR_DB_USER"),
        password=os.getenv("VECTOR_DB_PASSWORD")
    )
    return conn

# if __name__ == "__main__":
#     try:
#         conn = get_connection()
#         print("Connected to PostgreSQL successfully!")
#         conn.close()
#     except Exception as e:
#         print(f"Connection failed: {e}")


if __name__ == "__main__":
    try:
        conn = get_connection()
        print("Local PostgreSQL connected!")
        conn.close()

        conn2 = get_vector_connection()
        print("pgvector Docker DB connected!")
        conn2.close()
    except Exception as e:
        print(f"Connection failed: {e}")