
import os 
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()
def ingest_documents():
    loader=TextLoader("data/medical_docs.txt")
    documents= loader.load()
    splitter=RecursiveCharacterTextSplitter(
        separators=["\n\n","\n"," ",""],
        chunk_size=500,
        chunk_overlap=100
    )

    docs=splitter.split_documents(documents)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    CHROMA_PATH = os.path.join(BASE_DIR, "chroma_db")

    vector_store=Chroma.from_documents(
        docs,
        embedding=GoogleGenerativeAIEmbeddings(model="gemini-embedding-001"),
        persist_directory=CHROMA_PATH,
        collection_name="chat_chroma_db"
    )
  
    print(" Documents ingested successfully!")
if __name__=="__main__":
    ingest_documents()
