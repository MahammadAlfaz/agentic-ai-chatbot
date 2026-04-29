from app.llm.llm import get_llm
from app.rag.rag_state import RagState


def grade_docs_node(state:RagState)->RagState:
    llm=get_llm()
    question=state['transformed_querry']
    docs=state['retrieved_docs']

    if not docs:
        print("No docs to grade")
        return {
            'graded_docs':[]
        }
    relevant_docs =[]
    for doc in docs:
        prompt = f"""
        You are grading if a document is relevant to answer a medical question.
        
        Return ONLY "relevant" or "irrelevant".
        
        Question: {question}
        
        Document: {doc.page_content[:500]}
        
        Grade (relevant/irrelevant):
        """
        result=llm.invoke(prompt)

        grade=result.content.strip().lower()

        if "relevant" in grade and 'irrelevant' not in grade:
            relevant_docs.append(doc)
            print(f"Relevant:{doc.page_content[:80]}...")
        else:
            print(f"Irrelevant: {doc.page_content[:80]}...")
    print(f"Relevant docs:{len(relevant_docs)}/{len(docs)}")
    return {"graded_docs":relevant_docs}

