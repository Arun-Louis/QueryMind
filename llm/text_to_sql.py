from groq import Groq
from dotenv import load_dotenv
from db.connect import get_connection
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_schema():
    """Pull table and column names from the actual database."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT table_name, column_name, data_type
        FROM information_schema.columns
        WHERE table_schema = 'public'
        ORDER BY table_name, ordinal_position;
    """)

    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    # Format schema as readable text for the LLM
    schema = {}
    for table, column, dtype in rows:
        if table not in schema:
            schema[table] = []
        schema[table].append(f"{column} ({dtype})")

    schema_text = ""
    for table, columns in schema.items():
        schema_text += f"Table: {table}\n"
        schema_text += "  Columns: " + ", ".join(columns) + "\n\n"

    return schema_text

def generate_sql(question, schema_text):
    """Send schema + question to LLM, get SQL back."""
    prompt = f"""You are a SQL expert. Given the following PostgreSQL database schema, 
write a SQL query to answer the user's question.
Return ONLY the SQL query, no explanation, no markdown, no backticks.

Schema:
{schema_text}

Question: {question}

SQL:"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()

def run_query(sql):
    """Execute the generated SQL against the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    cursor.close()
    conn.close()
    return columns, rows

if __name__ == "__main__":
    print("Fetching schema...")
    schema_text = get_schema()

    question = "How many orders were placed each month in 2017?"

    print(f"\nQuestion: {question}")
    print("\nGenerating SQL...")
    sql = generate_sql(question, schema_text)
    print(f"\nGenerated SQL:\n{sql}")

    print("\nRunning query...")
    columns, rows = run_query(sql)
    print(f"\nColumns: {columns}")
    print("Results:")
    for row in rows:
        print(row) 