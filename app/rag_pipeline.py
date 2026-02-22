from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings

VECTOR_DB_PATH = "./vectordb"

def get_chain():
    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    vectordb = Chroma(
        persist_directory=VECTOR_DB_PATH,
        embedding_function=embeddings
    )

    retriever = vectordb.as_retriever(search_kwargs={"k": 8})

    llm = Ollama(
        model="phi3",
        temperature=0.1
    )

    # 🔥 STRICT GROUNDED PROMPT
    template = """
You are a financial assistant.
You MUST answer ONLY using the provided context.
Do NOT say you don't have access to the PDF.
Do NOT mention external databases.
If the answer is not found in context, say:
"Answer not found in provided document context."

Context:
{context}

Question:
{question}

Answer:
"""

    prompt = PromptTemplate(
        template=template,
        input_variables=["context", "question"]
    )

    chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=True
    )

    return chain