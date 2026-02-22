import os
from fastapi import FastAPI
from pydantic import BaseModel
from contextlib import asynccontextmanager

from app.data_ingestion import load_pdf
from app.rag_pipeline import get_chain
from app.prompts import OUTLINE_PROMPT, FORMULA_PROMPT, TEACH_PROMPT


PDF_PATH = "data/NISM_book.pdf"
VECTOR_DB_PATH = "./vectordb"


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ingest PDF only if vector DB does not exist
    if not os.path.exists(VECTOR_DB_PATH) or not os.listdir(VECTOR_DB_PATH):
        print("Vector DB not found. Running ingestion...")
        load_pdf(PDF_PATH)
    else:
        print("Vector DB found. Skipping ingestion.")

    # Load RAG chain once at startup
    app.state.chain = get_chain()

    yield

    # Optional cleanup logic can go here


app = FastAPI(
    title="Finance RAG Tutor",
    lifespan=lifespan
)


class TeachRequest(BaseModel):
    topic: str


@app.get("/toc")
def get_toc():
    result = app.state.chain.invoke({"query": OUTLINE_PROMPT})
    return {"toc": result["result"]}


@app.get("/formulae")
def get_formulae():
    result = app.state.chain.invoke({"query": FORMULA_PROMPT})
    print("Retrieved Context ")
    for doc in result["source_documents"]:
        print(doc.page.content[:300])
        print("-" * 50)
        
    return {"formulae": result["result"]}




@app.post("/teach")
def teach(req: TeachRequest):
    query = TEACH_PROMPT.format(topic=req.topic)
    result = app.state.chain.invoke({"query": query})
    return {"lesson": result["result"]}