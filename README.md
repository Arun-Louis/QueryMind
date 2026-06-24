# QueryMind — Hybrid NL2SQL + RAG Business Intelligence System

> Ask questions about your data in plain English. No SQL required.

---

## Overview

QueryMind is an AI-powered business intelligence system that combines two retrieval strategies:

- **Text-to-SQL** — converts natural language questions into SQL queries and runs them against a PostgreSQL database
- **RAG (Retrieval-Augmented Generation)** — searches business documents using semantic similarity via pgvector
- **Hybrid routing** — an LLM-based router classifies each question as SQL, RAG, or both, then merges the results into a single answer

Built on the [Olist Brazilian E-Commerce dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) (500k+ rows, 8 relational tables).

---

## Tech Stack

- **LLM** — LLaMA 3.1 8B via Groq API
- **Orchestration** — LangChain, LangGraph
- **Database** — PostgreSQL 14
- **Vector store** — pgvector
- **Embeddings** — sentence-transformers (all-MiniLM-L6-v2)
- **UI** — Streamlit + Plotly
- **Language** — Python 3.14

---

## How It Works

```
User question
    └── LLM Router (SQL / RAG / HYBRID)
            ├── SQL path: LangChain generates SQL → runs against PostgreSQL
            ├── RAG path: embeds question → pgvector similarity search → retrieves chunks
            └── Synthesizer: merges both results → final natural language answer
```

---

## Project Structure

```
querymind/
├── db/
│   ├── connect.py              # DB connection helpers
│   └── load_data.py            # Load Olist CSVs into PostgreSQL
├── llm/
│   ├── text_to_sql.py          # Phase 2 — raw LLM SQL pipeline
│   ├── langchain_sql.py        # Phase 3 — LangChain SQL chain
│   └── hybrid_pipeline.py      # Phase 5 — hybrid router
├── rag/
│   ├── create_reports.py       # Generate synthetic business PDFs
│   ├── embed_documents.py      # Chunk, embed, store in pgvector
│   └── retrieve.py             # Semantic retrieval
├── data/
│   └── reports/                # Business report PDFs
├── app.py                      # Streamlit UI
├── .env.example
├── requirements.txt
└── README.md
```

---

## Setup

### Prerequisites
- Python 3.10+
- PostgreSQL 14+
- Docker Desktop

### 1. Clone
```bash
git clone https://github.com/Arun-Louis/QueryMind.git
cd QueryMind
```

### 2. Virtual environment
```bash
python -m venv venv
venv\Scripts\activate       # Windows
source venv/bin/activate    # Mac/Linux
pip install -r requirements.txt
```

### 3. Environment variables
Create a `.env` file based on `.env.example`:
```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=nl2sql_db
DB_USER=postgres
DB_PASSWORD=your_password

VECTOR_DB_HOST=localhost
VECTOR_DB_PORT=5433
VECTOR_DB_NAME=nl2sql_db
VECTOR_DB_USER=postgres
VECTOR_DB_PASSWORD=your_password

GROQ_API_KEY=your_groq_api_key
```

### 4. Start pgvector (Docker)
```bash
docker run -d --name pgvector_db \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=nl2sql_db \
  -p 5433:5432 \
  pgvector/pgvector:pg14
```

### 5. Load data
Download the Olist dataset from Kaggle and place CSVs in `data/`, then:
```bash
python db/load_data.py
python -m rag.create_reports
python -m rag.embed_documents
```

### 6. Run
```bash
# Test pipeline
python -m llm.hybrid_pipeline

# Launch UI
streamlit run app.py
```

---

## Status

- [x] Phase 1 — Environment + data setup
- [x] Phase 2 — Raw LLM SQL generation
- [x] Phase 3 — LangChain SQL chain + conversation memory
- [x] Phase 4 — RAG layer with pgvector
- [x] Phase 5 — Hybrid router pipeline
- [ ] Phase 6 — Streamlit UI

---

## Dataset

[Olist Brazilian E-Commerce](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) — 100k orders, 8 relational tables covering orders, customers, products, sellers, payments, and reviews.

---

## Author

Arun Louis — [linkedin.com/in/arunlouis17](https://linkedin.com/in/arunlouis17)
