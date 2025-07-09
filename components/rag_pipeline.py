import os
from dotenv import load_dotenv

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import HuggingFaceHub
from langchain_ollama import OllamaEmbeddings
from langchain.chains import RetrievalQA
from langchain_core.documents import Document  # NEW import path for Document

import ollama

embeddings_model = OllamaEmbeddings(model="gemma:2b")

# Vector DB path
VECTOR_DB_PATH = r"VectorDB"


# Embed and store documents in FAISS

def create_vector_store(chunks):
    docs = [
        Document(page_content=chunk["text"], metadata=chunk["metadat"])
        for chunk in chunks
    ]

    db = FAISS.from_documents(docs,embeddings_model)
    db.save_lcoal(VECTOR_DB_PATH)
    return db

# Load existing vector store

def load_vector_store():
    return FAISS.load_local(VECTOR_DB_PATH,embeddings=embeddings_model)

def create_qa_chain():

    llm = ollama(model="llama2")

    vector_store = load_vector_store()
    retriever = vector_store.as_retriever(search_kwargs={"k":5})

    chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )

    return chain

def answer_question(question):
    chain = create_qa_chain()
    result = chain(question)
    return result