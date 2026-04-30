# 

# Complete RAG Pipeline — Detailed Flow with Examples
---

## Overview
This document provides a comprehensive walkthrough of a Retrieval-Augmented Generation (RAG) pipeline for medical question answering. The pipeline transforms user queries, retrieves relevant documents, validates content, and generates grounded answers with hallucination checking.

---

## Example Query
**User Input:** `"What is a heart attack?"` 

---

## Node 1 — Query Transformation
### Purpose
Rewrites the user's casual question into a search-optimized query.

### Why It's Needed
Vector databases work better with specific medical terminology than casual language.

### Prompt Sent to Gemini
```
You are an expert at reformulating medical questions for better search results.

Rewrite the following question to be more specific and search friendly.
Return ONLY the rewritten query, nothing else.

Original question: What is a heart attack?

Rewritten query:
```
### Gemini Response
```
Myocardial infarction symptoms causes treatment
```
### State After This Node
```json
{
  "question": "What is a heart attack?",
  "transformed_query": "Myocardial infarction symptoms causes treatment"
}
```
---

## Node 2 — Should I Retrieve?
### Purpose
Decides if this question needs document retrieval or can be answered directly.

### Why It's Needed
Simple questions like "hi" or "what is 2+2" don't need retrieval — saves time and API calls.

### Prompt Sent to Gemini
```
You are a medical assistant deciding if a question needs 
document retrieval to answer accurately.

Return ONLY "yes" or "no".

"yes" → question needs medical facts, drug info, 
         symptoms, treatments, or specific medical knowledge
"no"  → question is conversational, simple math, 
         greetings, or general knowledge

Question: Myocardial infarction symptoms causes treatment

Answer (yes/no):
```
### Gemini Response
```
yes
```
### State After This Node
```json
{
  "should_retrieve": true,
  "attempts": 0
}
```
---

## Node 3 — Multi Query Retrieval
### Purpose
Generates 4 different search queries and searches the vector store with each one. Merges and deduplicates results.

### Why It's Needed
One query misses relevant documents. Different phrasings catch different chunks.

### Prompt Sent to Gemini
```
Generate 4 different search queries to find medical information 
about the following topic.

Each query should focus on a different aspect.
Return ONLY the 4 queries, one per line, no numbering, no extra text.

Topic: Myocardial infarction symptoms causes treatment

Queries:
```
### Gemini Response
```
early warning signs of heart attack
risk factors for myocardial infarction development
acute myocardial infarction treatment guidelines
post-myocardial infarction recovery and rehabilitation
```
### Vector Store Searches
| Search | Query | Results |
| ----- | ----- | ----- |
| 1 | "early warning signs of heart attack" | 5 chunks |
| 2 | "risk factors for myocardial infarction" | 5 chunks |
| 3 | "acute myocardial infarction treatment" | 5 chunks |
| 4 | "post-myocardial infarction recovery" | 5 chunks |
**Total:** 20 chunks → deduplicate → **7 unique chunks**

### State After This Node
```json
{
  "retrieved_docs": [7 unique document chunks]
}
```
---

## Node 4 — Reranking
### Purpose
Scores each retrieved chunk by relevance to the original question. Keeps top 3.

### Why It's Needed
7 chunks is too many — some are loosely related. Reranking filters the best ones.

### Prompt Sent to Gemini (for each document)
```
Score how relevant this document is to the question.
Return ONLY a number between 0.0 and 1.0.

Question: What is a heart attack?

Document: HEART ATTACK (MYOCARDIAL INFARCTION)
A heart attack occurs when blood flow to a section 
of the heart muscle is blocked...

Relevance score (0.0 to 1.0):
```
### Scoring Results
| Chunk | Content Preview | Score | Status |
| ----- | ----- | ----- | ----- |
| 1 | "Symptoms: Chest pain, pressure..." | 1.0 | ✅ Kept |
| 2 | "HEART ATTACK (MYOCARDIAL INFARCTION)..." | 1.0 | ✅ Kept |
| 3 | "Symptoms That Suggest Serious Cause..." | 0.9 | ✅ Kept |
| 4 | "Risk Factors: High blood pressure..." | 0.2 | ❌ Removed |
| 5 | "Recovery: Cardiac rehabilitation..." | 0.2 | ❌ Removed |
| 6 | "Medical Treatment: Thrombolytics..." | 0.3 | ❌ Removed |
| 7 | "CHEST PAIN: Chest pain is a common..." | 0.9 | ❌ Removed (4th place) |
### State After This Node
```json
{
  "retrieved_docs": [top 3 chunks]
}
```
---

## Node 5 — Grade Documents (CRAG)
### Purpose
Reads each of the top 3 chunks and decides if they are actually useful to answer the question.

### Why It's Needed
Even highly ranked chunks might not directly answer the question. This is the final filter.

### Prompt Sent to Gemini (for each document)
```
You are grading if a document is relevant to answer a medical question.

Return ONLY "relevant" or "irrelevant".

Question: What is a heart attack?

Document: HEART ATTACK (MYOCARDIAL INFARCTION)
A heart attack occurs when blood flow to a section of the 
heart muscle is blocked, usually by a blood clot forming 
on plaque buildup in the coronary arteries...

Grade (relevant/irrelevant):
```
### Grading Results
| Chunk | Content Preview | Grade |
| ----- | ----- | ----- |
| 1 | "Symptoms: Chest pain..." | ✅ relevant |
| 2 | "HEART ATTACK (MYOCARDIAL)..." | ✅ relevant |
| 3 | "Symptoms That Suggest..." | ✅ relevant |
**Result:** 3/3 relevant

>  **Note:** If all chunks were irrelevant → Web Search would be triggered 

### State After This Node
```json
{
  "graded_docs": [3 verified relevant chunks]
}
```
---

## Node 6 — Web Search Fallback (CRAG)
### Trigger Condition
Only activated when `graded_docs` is empty — all chunks were irrelevant.

### Purpose
Searches the web using Tavily for real-time information.

### Example Scenario
```
Query: "What is the new 2024 heart attack treatment?"
→ Vector store has no recent info
→ All chunks graded irrelevant
→ Web search triggered
→ Tavily returns 3 fresh web results
→ Pipeline continues with web docs
```
### State After This Node (when triggered)
```json
{
  "graded_docs": [3 web search results],
  "web_search_used": true
}
```
>  **In our example:** Web search was **skipped** because documents were relevant. 

---

## Node 7 — Generate Answer
### Purpose
Uses the verified, relevant chunks as context to generate the final answer.

### Why It's Needed
Answer is grounded in verified sources — not LLM hallucination.

### Prompt Sent to Gemini
```
You are a medical assistant. Answer the question using ONLY 
the provided context. 

If the context doesn't contain enough information, say 
"I don't have enough information to answer this accurately."

Do NOT make up any medical facts.

Context:
Source 1:
Symptoms:
- Chest pain, pressure, tightness, or squeezing
- Pain radiating to left arm, jaw, neck, or back
- Shortness of breath
- Cold sweat
- Nausea or vomiting...

Source 2:
HEART ATTACK (MYOCARDIAL INFARCTION)
A heart attack occurs when blood flow to a section of the 
heart muscle is blocked for long enough that part of the 
heart muscle is damaged or dies...

Source 3:
Symptoms That Suggest Serious Cause:
- Crushing or squeezing chest pain
- Pain radiating to arm, jaw, neck, or back...

Question: What is a heart attack?

Answer:
```
### Gemini Response
```
A heart attack, also known as myocardial infarction, occurs 
when blood flow to a section of the heart muscle is blocked, 
usually by a blood clot. This causes the heart muscle to be 
damaged or die.

Common symptoms include:
- Chest pain or pressure
- Pain radiating to the left arm or jaw
- Shortness of breath
- Cold sweat and nausea

It is a medical emergency requiring immediate treatment.
```
### State After This Node
```json
{
  "generated_answer": "A heart attack, also known as...",
  "attempts": 1
}
```
---

## Node 8 — Hallucination Grader
### Purpose
Checks if every claim in the generated answer is supported by the source documents.

### Why It's Needed
LLMs can add extra facts not in the context — dangerous for a medical app.

### Prompt Sent to Gemini
```
You are a medical fact checker. 

Check if the answer is fully supported by the provided context.

Score the answer between 0.0 and 1.0:
1.0 → every claim is supported by context
0.7 → most claims supported, minor gaps
0.5 → some claims supported, some not
0.0 → answer not supported by context at all

Return ONLY a number between 0.0 and 1.0, nothing else.

Context:
Source 1: Symptoms: Chest pain, pressure...
Source 2: HEART ATTACK (MYOCARDIAL INFARCTION)...
Source 3: Symptoms That Suggest Serious Cause...

Question: What is a heart attack?

Answer to check:
A heart attack, also known as myocardial infarction, occurs 
when blood flow to a section of the heart muscle is blocked...+

Score:
```
### Gemini Response
```
1.0
```
### State After This Node
```json
{
  "hallucination_score": 1.0
}
```
---

## Node 9 — Decision (Hallucination Router)
### Purpose
Decides what to do based on the hallucination score.

### Routing Logic
```python
score >= 0.7  → "good"      → return answer to user ✅
score < 0.7   
  attempts < 3 → "regenerate" → go back to Node 7
  attempts >= 3 → "give_up"   → return answer anyway
```
### Decision in Our Example
| Metric | Value | Result |
| ----- | ----- | ----- |
| Score | 1.0 | ≥ 0.7 |
| Decision | `"good"`  | ✅ Return answer |
---

## Final Output to User
```json
{
  "output": "A heart attack, also known as myocardial 
             infarction, occurs when blood flow to a 
             section of the heart muscle is blocked...",
  "intent": "rag",
  "status": "Ok"
}
```
---

## Complete Flow Summary
```
"What is a heart attack?"
          ↓
① Query Transformation  → "Myocardial infarction symptoms causes treatment"
          ↓
② Should Retrieve?      → YES
          ↓
③ Multi Query           → 4 queries → 7 unique chunks
          ↓
④ Reranking             → scored 7 chunks → kept top 3 (scores: 1.0, 1.0, 0.9)
          ↓
⑤ Grade Docs            → 3/3 relevant ✅
          ↓
⑥ Web Search            → skipped (docs were relevant)
          ↓
⑦ Generate Answer       → grounded answer from verified sources
          ↓
⑧ Hallucination Score   → 1.0 ✅
          ↓
⑨ Decision              → "good" → return answer
          ↓
✅ Final Answer returned on attempt 1
```
---

## Key Pipeline Features
| Feature | Benefit |
| ----- | ----- |
| **Query Transformation** | Improves retrieval accuracy with medical terminology |
| **Retrieval Decision** | Saves resources on simple queries |
| **Multi-Query Retrieval** | Captures diverse relevant documents |
| **Reranking** | Filters to most relevant chunks |
| **CRAG Grading** | Validates document relevance |
| **Web Search Fallback** | Handles knowledge gaps |
| **Hallucination Checking** | Ensures factual accuracy |
| **Retry Mechanism** | <p>Improves answer quality through regeneration</p><p></p> |


