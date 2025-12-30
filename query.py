# query.py

import json

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms import Ollama

from prompts import RAG_PROMPT, AI_TWIN_IDENTITY
from config import *
from memory import load_memory, save_memory
from tools import list_files, read_memory, clear_memory


# ---------- SETUP ----------
embeddings = OllamaEmbeddings(model=EMBED_MODEL)

db = Chroma(
    persist_directory=VECTOR_DB_DIR,
    embedding_function=embeddings
)

retriever = db.as_retriever(search_kwargs={"k": TOP_K})

llm = Ollama(
    model=LLM_MODEL,
    temperature=0
)

memory = load_memory()


# ---------- TOOL ROUTER ----------
def tool_router(user_input: str):
    prompt = f"""
You are a tool selector.

Available tools:
- list_files
- read_memory
- clear_memory
- none

User request:
"{user_input}"

Rules:
- If user wants to see files → list_files
- If user wants to view memory → read_memory
- If user wants to reset memory → clear_memory
- Otherwise → none

Return ONLY JSON:
{{
  "tool": "list_files|read_memory|clear_memory|none"
}}
"""
    response = llm.invoke(prompt)

    try:
        return json.loads(response)["tool"]
    except Exception:
        return "none"


# ---------- MAIN LOOP ----------
while True:
    query = input("\n🧠 Ask AI Twin (or 'exit'): ").strip()

    if query.lower() == "exit":
        break

    tool = tool_router(query)

    if tool == "list_files":
        result = list_files()
        print("\n🤖 AI Twin:\n Files in project:")
        for f in result:
            print(" -", f)
        continue

    if tool == "read_memory":
        print("\n🤖 AI Twin:\n Current memory:")
        print(json.dumps(read_memory(), indent=2))
        continue

    if tool == "clear_memory":
        print("\n🤖 AI Twin:\n", clear_memory())
        continue

    # ---- MEMORY QUESTIONS ----
    if "what is my name" in query.lower():
        name = memory["profile"].get("name")
        print(f"\n🤖 AI Twin:\n Your name is {name}." if name else "\n🤖 AI Twin:\n I don't know your name yet.")
        continue

    # ---- CHAT ----
    if any(x in query.lower() for x in ["hi", "hello", "hey", "who are you"]):
        answer = llm.invoke(f"{AI_TWIN_IDENTITY}\nUser: {query}")
        print("\n🤖 AI Twin:\n", answer)
        continue

    # ---- RAG ----
    docs = retriever.invoke(query)
    context = "\n\n".join(d.page_content for d in docs)

    prompt = RAG_PROMPT.format(
        identity=AI_TWIN_IDENTITY,
        context=context,
        question=query
    )

    answer = llm.invoke(prompt)
    print("\n🤖 AI Twin:\n", answer)
