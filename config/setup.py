import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_chroma import Chroma
from chromadb.config import Settings

load_dotenv()

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
llm = ChatGroq(model="llama3-70b-8192")

chroma_settings = Settings(
    persist_directory="chroma_legal_db",
    anonymized_telemetry=False
)

vectorstore = Chroma(
    persist_directory="chroma_legal_db",
    embedding_function=embedding_model,
    client_settings=chroma_settings
)

retriever = vectorstore.as_retriever()
