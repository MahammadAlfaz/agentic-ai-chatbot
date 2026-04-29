from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os

load_dotenv()

def get_retriever():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    CHROMA_PATH = os.path.join(BASE_DIR, "chroma_db")
    vector_db=Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=GoogleGenerativeAIEmbeddings(model="gemini-embedding-001"),
        collection_name="chat_chroma_db"
    )
    return vector_db.as_retriever(search_kwargs={"k": 5})