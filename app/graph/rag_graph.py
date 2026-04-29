from langgraph.graph import END, START, StateGraph

from app.nodes.generate_answers import generate_answer_node
from app.nodes.grade_docs import grade_docs_node
from app.nodes.hallucination_grader import hallucination_grader_node
from app.nodes.multi_query_retrieval import multi_query_retrieval_node
from app.nodes.query_transformer import query_transform_node
from app.nodes.reranking import reranking_node
from app.nodes.should_retrive import should_retrieve_node
from app.nodes.web_search import web_search_node
from app.rag.rag_state import RagState


def should_retrieve_router(state:RagState)->str:
    if state['should_retrieve']:
        return 'retrieve'
    return 'skip_retrieve'


def docs_router(state:RagState)->str:
    if not state['graded_docs']:
        return 'web_search'
    return 'generate'


def hallucination_router(state:RagState)->str:
    score=state['hallucination_score']
    attempts=state.get('attempts',0)

    if float(score) >=0.7:
        return 'good'
    elif attempts >=3:
        return 'give_up'
    else:
        return 'regenerate'
    
def build_rag_graph():
    graph=StateGraph(RagState)
    
    graph.add_node("query_transformation",query_transform_node)
    graph.add_node("should_retrieve",should_retrieve_node)
    graph.add_node("multi_query_retrieval",multi_query_retrieval_node)
    graph.add_node("reranking",reranking_node)
    graph.add_node("grade_docs",grade_docs_node)
    graph.add_node("web_search",web_search_node)
    graph.add_node("generate_answer",generate_answer_node)
    graph.add_node("hallucination_grader",hallucination_grader_node)

    graph.add_edge(START,'query_transformation')
    graph.add_edge("query_transformation","should_retrieve")
    graph.add_edge("multi_query_retrieval","reranking")
    graph.add_edge("reranking","grade_docs")
    graph.add_edge("web_search","generate_answer")
    graph.add_edge("generate_answer","hallucination_grader")
    

    graph.add_conditional_edges(
        'should_retrieve',
        should_retrieve_router,{
            "retrieve":"multi_query_retrieval",
            "skip_retrieve":"generate_answer"
        }
    )

    graph.add_conditional_edges(
        "grade_docs",
        docs_router,{
            "web_search":"web_search",
            "generate":"generate_answer"
        }
    )

    graph.add_conditional_edges(
        "hallucination_grader",
        hallucination_router,{
            "good":END,
            "give_up":END,
            "regenerate":"generate_answer"
        }

    )
    return graph.compile()

rag_workflow=build_rag_graph()