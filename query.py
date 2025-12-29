# query.py

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms import Ollama
from prompts import RAG_PROMPT
from config import *

embeddings = OllamaEmbeddings(model=EMBED_MODEL)

db = Chroma(
    persist_directory=VECTOR_DB_DIR,
    embedding_function=embeddings
)

retriever = db.as_retriever(
    search_kwargs={"k": TOP_K}
)

llm = Ollama(
    model=LLM_MODEL,
    temperature=TEMPERATURE
)

while True:
    query = input("\n🧠 Ask AI Twin (or 'exit'): ")
    if query.lower() == "exit":
        break

    docs = retriever.get_relevant_documents(query)
    context = "\n\n".join(d.page_content for d in docs)

    prompt = RAG_PROMPT.format(
        context=context,
        question=query
    )

    answer = llm.invoke(prompt)
    print("\n🤖 AI Twin:\n", answer)
