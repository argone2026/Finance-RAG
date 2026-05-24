"""
ingest.py — loads a PDF, chunks it, embeds it, stores in ChromaDB
Run once per PDF: python -m app.ingest --file data/statement.pdf
"""
import argparse
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

CHROMA_PATH = "chroma_db"
EMBED_MODEL = "all-MiniLM-L6-v1"  # smaller model, ~22MB vs 80MB for v2


def ingest(pdf_path: str):
    print(f"Loading: {pdf_path}")
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    if not documents:
        raise ValueError(f"No text could be extracted from {pdf_path}. Make sure it's a valid PDF with readable text.")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
    )
    chunks = splitter.split_documents(documents)
    print(f"Created {len(chunks)} chunks")

    if not chunks:
        raise ValueError("No chunks were created from the PDF. The document may be empty or too short.")

    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)

    db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_PATH,
    )
    db.persist()
    print(f"Stored in ChromaDB at ./{CHROMA_PATH}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True, help="Path to PDF")
    args = parser.parse_args()
    ingest(args.file)