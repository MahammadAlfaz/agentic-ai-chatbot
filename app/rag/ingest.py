
import os 
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.rag.google_docs_loader import load_from_google_doc

load_dotenv()
def ingest_documents(folder_id:str=None,source:str ="local"):
    if  source.lower().strip() == "google_docs":
        if not folder_id:
            raise ValueError("folder id is required ")
        print(f"Loading from Google Drive folder: {folder_id}")
        documents=load_from_google_doc(folder_id)
    else:
        print("Loading from local file...")
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
    ingest_documents(folder_id="1pyAO-jmiHiJahq_2VFspJdCTmCcwJJQQ",source="google_docs")
