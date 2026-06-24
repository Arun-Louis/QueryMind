from sentence_transformers import SentenceTransformer
from pypdf import PdfReader
from dotenv import load_dotenv
from db.connect import get_vector_connection
import os
import re

load_dotenv()

# Load the embedding model — downloads once, cached locally after that
# all-MiniLM-L6-v2 produces 384-dimensional vectors, fast and accurate enough for our use case
print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")
print("Model loaded.")

def extract_text_from_pdf(filepath):
    """Read all text from a PDF file."""
    reader = PdfReader(filepath)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def chunk_text(text, chunk_size=500, overlap=50):
    """
    Split text into overlapping chunks.
    chunk_size: how many characters per chunk
    overlap: how many characters to repeat between chunks
    This ensures sentences at boundaries aren't lost.
    """
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        if chunk.strip():  # skip empty chunks
            chunks.append(chunk.strip())
        start = end - overlap  # overlap with previous chunk
    return chunks

def setup_vector_table(conn):
    """Create the table that stores document chunks and their embeddings."""
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS document_chunks (
            id SERIAL PRIMARY KEY,
            filename TEXT,
            chunk_index INTEGER,
            content TEXT,
            embedding vector(384)
        );
    """)
    conn.commit()
    cursor.close()
    print("document_chunks table ready.")

def embed_and_store(conn, filepath):
    """Extract text, chunk it, embed each chunk, store in pgvector."""
    filename = os.path.basename(filepath)
    print(f"\nProcessing {filename}...")

    # Step 1 — extract text
    text = extract_text_from_pdf(filepath)
    print(f"  Extracted {len(text)} characters")

    # Step 2 — chunk the text
    chunks = chunk_text(text)
    print(f"  Split into {len(chunks)} chunks")

    # Step 3 — embed all chunks at once (batch is faster)
    embeddings = model.encode(chunks)
    print(f"  Generated {len(embeddings)} embeddings of dimension {len(embeddings[0])}")

    # Step 4 — store each chunk + embedding in pgvector
    cursor = conn.cursor()

    # Delete existing chunks for this file so we don't duplicate on re-run
    cursor.execute("DELETE FROM document_chunks WHERE filename = %s", (filename,))

    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        cursor.execute("""
            INSERT INTO document_chunks (filename, chunk_index, content, embedding)
            VALUES (%s, %s, %s, %s)
        """, (filename, i, chunk, embedding.tolist()))

    conn.commit()
    cursor.close()
    print(f"  Stored {len(chunks)} chunks in pgvector")

if __name__ == "__main__":
    conn = get_vector_connection()

    # Create the table
    setup_vector_table(conn)

    # Process all PDFs in data/reports/
    reports_dir = "data/reports"
    for filename in os.listdir(reports_dir):
        if filename.endswith(".pdf"):
            filepath = os.path.join(reports_dir, filename)
            embed_and_store(conn, filepath)

    conn.close()
    print("\nAll documents embedded and stored successfully!")