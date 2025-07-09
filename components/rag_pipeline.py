import os
from dotenv import load_dotenv

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import HuggingFaceHub
from langchain.chains import RetrievalQA
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings, OllamaLLM

# ✅ Optional if you use .env
# load_dotenv()

# 🧠 Load Ollama embeddings
embeddings_model = OllamaEmbeddings(model="gemma:2b")

# Vector DB path
VECTOR_DB_PATH = "VectorDB"

# Embed and store documents in FAISS
def create_vector_store(chunks):
    try:
        docs = [
            Document(page_content=chunk["text"], metadata=chunk["metadata"])
            for chunk in chunks
        ]

        print(f"[INFO] Creating FAISS DB with {len(docs)} docs...")

        db = FAISS.from_documents(docs, embeddings_model)

        if not os.path.exists(VECTOR_DB_PATH):
            os.makedirs(VECTOR_DB_PATH)

        db.save_local(VECTOR_DB_PATH)
        print("[✅] Vector DB saved successfully.")

    except Exception as e:
        print("❌ Failed to create vector store:", e)
        import traceback
        traceback.print_exc()


# Load existing vector store
def load_vector_store():
    return FAISS.load_local(VECTOR_DB_PATH, embeddings=embeddings_model, allow_dangerous_deserialization=True)

# Create a QA chain
def create_qa_chain():
    llm = OllamaLLM(model="mistral")  # ✅ Correct usage — this is the LangChain class now
    vector_store = load_vector_store()
    retriever = vector_store.as_retriever(search_kwargs={"k": 5})
    chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )
    return chain

# Answer a user question
def answer_question(question):
    chain = create_qa_chain()
    result = chain.run(question)  # ✅ use .run() instead of calling directly
    return result
