from dotenv import load_dotenv
from langchain_google_community import GoogleDriveLoader

load_dotenv()
def load_from_google_doc(folder_id:str):
    """
    Load content from a Google Doc using service account credentials.
    
    Args:
        document_id: The ID from the Google Doc URL
        https://docs.google.com/document/d/DOCUMENT_ID_HERE/edit
    """
   
   
    loader = GoogleDriveLoader(
    folder_id=folder_id,
    credentials_path="C:/Projects/agentic-ai-chatbot/credential.json",
    token_path="C:/Projects/agentic-ai-chatbot/token.json",
    scopes=["https://www.googleapis.com/auth/drive.readonly"],
    file_types=["document"], 
    recursive=False 
    )

    docs=loader.load()
   
    if not docs:
        print("No docs found!")
        return []
    
    print(docs[0].page_content[:200])
    return docs