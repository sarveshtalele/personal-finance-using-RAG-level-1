import os 
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma


VECTOR_DB_PATH= "./vectordb"

def load_pdf(pdf_path: str):
    if not os.path.exists(pdf_path):
        raise FileNotFoundError("Unable to load PDF file!")
    
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(docs)

    embeddings = OllamaEmbeddings(model='nomic-embed-text')

    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory= VECTOR_DB_PATH
    )

    vectordb.persist()