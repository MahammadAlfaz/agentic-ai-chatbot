from typing import List, TypedDict


class RagState(TypedDict):
    question:str
    transformed_querry:str
    should_retrieve:bool
    retrieved_docs:List[str]
    graded_docs:List[str]
    web_search_used:bool
    generated_answer:str
    hallucination_score:float
    attempts:int 
    final_answer:str
