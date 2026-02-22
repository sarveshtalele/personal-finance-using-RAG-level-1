# Personal Finance RAG — Professional README

Compact Retrieval-Augmented Generation (RAG) demo for financial learning. The project pairs a Streamlit front-end with a FastAPI backend that provides RAG capabilities via LangChain, Ollama (local LLM + embeddings), and Chroma for vector storage.


## Key Features

- Streamlit UI (`streamlit_app.py`) — Table of Contents, Formula Explorer, Conversational Tutor.

- FastAPI backend (`app/main.py`) — endpoints: `/toc`, `/formulae`, `/teach`.

- RAG pipeline (`app/rag_pipeline.py`) — LangChain retrieval, Ollama LLM, Chroma vector store.
- PDF ingestion (`app/data_ingestion.py`) — loads PDFs, chunking, embedding, and persists `vectordb/`.



**Repository layout (top-level)**

- `streamlit_app.py` — Streamlit front-end
- `app/main.py` — FastAPI app + startup lifecycle
- `app/rag_pipeline.py` — RAG chain construction
- `app/data_ingestion.py` — PDF loader + persistence
- `requirements.txt` — Python dependencies
- `data/` — source PDFs (e.g., `data/NISM_book.pdf`)
- `vectordb/` — persistent Chroma DB directory (created by ingestion)


## Architecture

Overview: the app is split into three primary layers: Presentation, API, and Retrieval. Each layer is decoupled so you can replace components independently (e.g., swap Ollama for a different LLM provider).

- Presentation (Streamlit): `streamlit_app.py` provides a web UI that calls the FastAPI backend for content (TOC, formulas, lessons).
- API (FastAPI): `app/main.py` manages startup lifecycle; on first run it triggers ingestion (if `vectordb/` is missing) and creates a shared RAG chain instance in `app.state.chain`.
- Retrieval (RAG): `app/rag_pipeline.py` wires embeddings, Chroma vector store, and the Ollama LLM into a `RetrievalQA` chain. The chain returns grounded responses plus source documents.

### Sequence (startup + query flow):

1. Developer starts FastAPI: `uvicorn app.main:app`.
2. `app.main` lifespan checks `vectordb/`; if empty it calls `load_pdf()` in `app/data_ingestion.py`.
3. `load_pdf()` loads PDF(s), splits into chunks, computes embeddings via OllamaEmbeddings, and writes Chroma data to `vectordb/`.
4. `app.main` initializes the RAG chain (`get_chain()`), storing it in `app.state.chain`.
5. Streamlit UI issues HTTP requests to FastAPI endpoints (`/toc`, `/formulae`, `/teach`).
6. FastAPI uses the chain to answer queries, returning grounded results to the UI.


## Requirements & Prerequisites

- Python 3.11+ (project used Python 3.12 during development).
- System: macOS / Linux / Windows (Docker-friendly).
- Ollama installed and running locally with the models referenced in the code (`phi3` for LLM and `nomic-embed-text` for embeddings). See Ollama docs for installation and model management.

Install Python deps:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```



## Configuration

- API base in the UI: `streamlit_app.py` uses `API_BASE = "http://127.0.0.1:8000"`. Change this if your backend runs elsewhere.
- Default PDF path: `app/main.py` references `data/NISM_book.pdf`. Replace or add PDFs in `data/` as needed.
- Vector DB path: `vectordb/` (persisted by `app/data_ingestion.py` and consumed by `app/rag_pipeline.py`).



## Running the project (development)

1) Start the FastAPI backend (will run ingestion if `vectordb/` is empty):

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

2) Start the Streamlit UI in another terminal:

```bash
streamlit run streamlit_app.py
```

Open the Streamlit URL shown in the terminal. The UI communicates with FastAPI at `http://127.0.0.1:8000` by default.



## Development notes

- Rebuild embeddings / force re-ingestion: stop the backend, delete or rename `vectordb/`, then restart the FastAPI server.

- Replace LLM or embeddings: update `app/rag_pipeline.py` to use a different `llm` or `embeddings` implementation.

- Logging: `app/main.py` prints ingestion progress and source snippets for debugging; consider adding structured logging.



## Troubleshooting

- Ollama connection errors: verify Ollama daemon is running and models are installed. Test locally with the `ollama` CLI.
- Missing PDF: ensure the file at `data/NISM_book.pdf` exists and is readable.
- Chroma errors: remove `vectordb/` to force re-ingestion, or inspect permissions.


## Next steps / Improvements

- Add health/readiness endpoints for Ollama and Chroma in `app/main.py`.
- Add a small demo dataset and an automated script to populate `data/` and run ingestion for CI or demos.
- Add tests for the RAG chain responses and retrieval quality.


## License

An `LICENSE` file was added to this repository (MIT). See `LICENSE` at the project root.


