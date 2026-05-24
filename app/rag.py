"""
rag.py — retrieves relevant chunks and calls Groq to answer a question
"""
import os
from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_groq import ChatGroq

load_dotenv()

CHROMA_PATH = "chroma_db"
EMBED_MODEL = "all-MiniLM-L6-v2"
TOP_K = 5  # how many chunks to retrieve

llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.1-8b-instant",
    temperature=0.7
)


def build_prompt(question: str, context_chunks: list[str]) -> str:
    context = "\n\n---\n\n".join(context_chunks)
    return f"""You are a helpful financial assistant.
Use ONLY the context below (extracted from a bank statement) to answer the question.
If the answer is not in the context, say "I couldn't find that in your statement."

CONTEXT:
{context}

QUESTION: {question}

ANSWER:"""


def ask(question: str) -> dict:
    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)

    results = db.similarity_search_with_score(question, k=TOP_K)
    chunks = [doc.page_content for doc, _score in results]

    prompt = build_prompt(question, chunks)
    response = llm.invoke(prompt)

    return {
        "answer": response.content,
        "sources": chunks,
    }