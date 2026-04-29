

from dotenv import load_dotenv
from langchain_community.tools import TavilySearchResults
from langchain_core.documents import Document

from app.rag.rag_state import RagState


load_dotenv()

def web_search_node(state:RagState)->RagState:
    question=state['transformed_querry']

    print(f"No relevant docs found - searching web for: {question}")

    web_search_tool=TavilySearchResults(max_results=3)
    results=web_search_tool.invoke(question)

    web_docs=[
        Document(
            page_content=result['content'],
            metadata={
                'source':result['url'],
                'web_search':True
            }
        )
        for result in results
        if result.get('content')
    ]
    print(f"Web search returned {len(web_docs)} docs")

    return {
        "graded_docs":web_docs,
        "web_search_used":True
    }