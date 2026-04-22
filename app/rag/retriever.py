from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings



def get_retriever():
    vector_db=Chroma(
        persist_directory="chroma_db",
        embedding_function=GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")
    )
    return vector_db.as_retriever()