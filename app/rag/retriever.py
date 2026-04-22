from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

def get_retriever():
    vector_db=Chroma(
        persist_directory="chroma_db",
        embedding_function=GoogleGenerativeAIEmbeddings(model="gemini-embedding-001"),
        collection_name="chat_chroma_db"
    )
    return vector_db.as_retriever(search_kwargs={"k": 2})