from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI


load_dotenv()

def get_llm(provider: str="gemini", model:str="gemini-2.5-flash-lite"):
    if provider=="gemini":
        return ChatGoogleGenerativeAI(model=model or "gemini-2.5-flash-lite")
    elif provider =="openai":
        return ChatOpenAI(model=model or "gpt-4o",temperature=0.7)
    else :
        raise ValueError("Unsupported LLM ")


