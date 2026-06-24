\# QueryMind — Hybrid NL2SQL + RAG Business Intelligence System



A natural language BI tool that lets non-technical users query a PostgreSQL database and retrieve document context using plain English. No SQL knowledge required.



\## What it does



Type a question like \*"Why did sales drop in Q3 2017?"\* and QueryMind:

1\. Classifies it as SQL, RAG, or Hybrid

2\. Queries your PostgreSQL database for numbers

3\. Searches business report PDFs for context

4\. Merges both into one coherent answer



\## Architecture



| Layer | Technology |

|---|---|

| LLM | LLaMA 3.1 8B via Groq API |

| SQL generation | LangChain SQLDatabaseChain |

| Vector search | pgvector (PostgreSQL extension) |

| Embeddings | sentence-transformers (all-MiniLM-L6-v2) |

| Orchestration | LangChain + LangGraph |

| Dataset | Olist Brazilian E-Commerce (500k+ rows, 8 tables) |

| UI | Streamlit + Plotly |



\## Project Structure



```

querymind/

├── db/

│   ├── connect.py          # PostgreSQL + pgvector connections

│   └── load\_data.py        # Load Olist CSVs into PostgreSQL

├── llm/

│   ├── text\_to\_sql.py      # Phase 2 — raw LLM SQL generation

│   ├── langchain\_sql.py    # Phase 3 — LangChain SQL chain

│   └── hybrid\_pipeline.py  # Phase 5 — full hybrid router

├── rag/

│   ├── create\_reports.py   # Generate synthetic PDF reports

│   ├── embed\_documents.py  # Chunk, embed, store in pgvector

│   └── retrieve.py         # Semantic similarity retrieval

├── data/

│   └── reports/            # Synthetic business PDFs

├── app.py                  # Streamlit UI (Phase 6)

├── .env.example            # Environment variable template

├── requirements.txt

└── README.md

```



\## Setup



\### Prerequisites

\- Python 3.10+

\- PostgreSQL 14+

\- Docker Desktop



\### 1. Clone the repo

```bash

git clone https://github.com/Arun-Louis/querymind.git

cd querymind

```



\### 2. Create virtual environment

```bash

python -m venv venv

venv\\Scripts\\activate        # Windows

source venv/bin/activate     # Mac/Linux

```



\### 3. Install dependencies

```bash

pip install -r requirements.txt

```



\### 4. Set up environment variables

Copy `.env.example` to `.env` and fill in your values:

```

DB\_HOST=localhost

DB\_PORT=5432

DB\_NAME=nl2sql\_db

DB\_USER=postgres

DB\_PASSWORD=your\_password



VECTOR\_DB\_HOST=localhost

VECTOR\_DB\_PORT=5433

VECTOR\_DB\_NAME=nl2sql\_db

VECTOR\_DB\_USER=postgres

VECTOR\_DB\_PASSWORD=your\_password



GROQ\_API\_KEY=your\_groq\_api\_key

```



\### 5. Download the dataset

Download the Olist Brazilian E-Commerce dataset from Kaggle:

https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

Place the CSV files in data/



\### 6. Start pgvector with Docker

```bash

docker run -d --name pgvector\_db \\

&#x20; -e POSTGRES\_PASSWORD=postgres \\

&#x20; -e POSTGRES\_DB=nl2sql\_db \\

&#x20; -p 5433:5432 \\

&#x20; pgvector/pgvector:pg14

```



\### 7. Load data and build RAG index

```bash

python db/load\_data.py

python -m rag.create\_reports

python -m rag.embed\_documents

```



\### 8. Run

```bash

\# Test the pipeline

python -m llm.hybrid\_pipeline



\# Launch UI

streamlit run app.py

```



\## How the router works



Every question is classified by the LLM into one of three paths:



\- \*\*SQL\*\* — needs numbers, counts, rankings from the database

\- \*\*RAG\*\* — needs qualitative context or explanations from documents

\- \*\*HYBRID\*\* — needs both; results are merged into one answer



\## Status



\- \[x] Phase 1 — Environment + data setup

\- \[x] Phase 2 — Raw LLM SQL generation

\- \[x] Phase 3 — LangChain SQL chain + conversation memory

\- \[x] Phase 4 — RAG layer with pgvector

\- \[x] Phase 5 — Hybrid pipeline with router

\- \[ ] Phase 6 — Streamlit UI

