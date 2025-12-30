# ingest.py

# ingest.py

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    DirectoryLoader
)

from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

from config import *

print("📥 Loading documents...")

loader = DirectoryLoader(
    DATA_DIR,
    glob="**/*.*",
    show_progress=True
)

docs = loader.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP
)

chunks = splitter.split_documents(docs)

print(f"✂️ Chunks created: {len(chunks)}")

embeddings = OllamaEmbeddings(model=EMBED_MODEL)

db = Chroma.from_documents(
    chunks,
    embedding=embeddings,
    persist_directory=VECTOR_DB_DIR
)

db.persist()

print("✅ AI Twin memory created successfully")
