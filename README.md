# 🏥 Agentic AI Medical Chatbot

A multi-agent AI chatbot for medical queries, powered by **LangGraph**, **Google Gemini**, and **FastAPI**. The system intelligently routes queries through specialized agents, supports human-in-the-loop approval for sensitive requests, and uses an advanced RAG pipeline with hallucination grading.

---

## 🗂️ Project Structure

```
agentic-ai-chatbot/
├── app/
│   ├── api/
│   │   └── routes.py           # FastAPI route handlers
│   ├── graph/
│   │   ├── agent_graph.py      # Main LangGraph agent graph
│   │   ├── rag_graph.py        # Advanced RAG sub-graph
│   │   ├── state.py            # Agent state schema
│   │   └── basic_graph.py      # Simple graph example
│   ├── nodes/
│   │   ├── intent_node.py      # Query intent classification
│   │   ├── llm_node.py         # General LLM conversation node
│   │   ├── mcp_node.py         # MCP tool node (medicine lookup)
│   │   ├── rag_node.py         # RAG retrieval node
│   │   ├── tool_node.py        # Symptom checker tool node
│   │   ├── stream_node.py      # Streaming response node
│   │   ├── generate_answers.py # RAG answer generation
│   │   ├── grade_docs.py       # Document relevance grader
│   │   ├── hallucination_grader.py  # Hallucination detection
│   │   ├── multi_query_retrieval.py # Multi-query retriever
│   │   ├── query_transformer.py     # Query rewriting
│   │   ├── reranking.py        # Document reranker
│   │   ├── should_retrive.py   # Retrieval decision node
│   │   └── web_search.py       # Tavily web search fallback
│   ├── llm/
│   │   └── llm.py              # LLM factory (Gemini / OpenAI)
│   ├── mcp_client/
│   │   └── client.py           # Multi-server MCP client
│   ├── mcp_server/
│   │   ├── server.py           # FastMCP server (OpenFDA integration)
│   │   └── schemas.py          # Medicine response schema
│   ├── memory/
│   │   ├── memory.py           # Chat memory helpers
│   │   └── store.py            # JSON file-based memory store
│   ├── models/
│   │   ├── request.py          # Request Pydantic models
│   │   └── response.py         # Response Pydantic models
│   ├── rag/
│   │   ├── google_docs_loader.py  # Google Drive document loader
│   │   ├── ingest.py           # Document ingestion pipeline
│   │   ├── rag_state.py        # RAG state schema
│   │   └── retriever.py        # Chroma vector store retriever
│   └── tools/
│       ├── medicine_info.py    # Medicine info LangChain tool
│       ├── symptoms_checker.py # Symptom analysis LangChain tool
│       ├── schemas.py          # Tool output schemas
│       └── tools.py            # Tool registry
├── data/
│   └── chat_memory/            # Per-session chat history (JSON)
├── chroma_db/                  # Chroma vector store (auto-generated)
├── credential.json             # Google OAuth credentials
├── token.json                  # Google OAuth token (auto-generated)
└── main.py                     # FastAPI app entrypoint
```

---

## ✨ Features

### 🧠 Intelligent Intent Routing
Queries are classified into one of four intents and routed to the appropriate agent:

| Intent | Handler | Description |
|--------|---------|-------------|
| `medicine` | `mcp_node` | Fetches real drug data from OpenFDA via MCP |
| `symptom` | `tool_node` | Analyzes symptoms using structured LLM tools |
| `rag` | `rag_node` | Answers medical questions using retrieved documents |
| `general` | `llm_node` | General conversation with session memory |

### 🔒 Human-in-the-Loop Approval
Medicine queries (`mcp_node`) require human approval before executing. The graph pauses with `interrupt_before`, allowing an operator to approve or reject via dedicated endpoints.

### 📚 Advanced RAG Pipeline
The RAG sub-graph includes:
- **Query Transformation** — rewrites the user query for better retrieval
- **Should Retrieve** — decides if retrieval is needed
- **Multi-Query Retrieval** — generates 4 query variants for broader coverage
- **Reranking** — LLM-scored relevance ranking
- **Document Grading** — filters irrelevant chunks
- **Web Search Fallback** — uses Tavily if no relevant docs are found
- **Hallucination Grading** — scores the answer against retrieved context (retries up to 3×)

### 🔄 Streaming Support
Real-time token streaming via Server-Sent Events (SSE).

### 🗄️ Knowledge Sources
- **Local files** — ingest from `data/medical_docs.txt`
- **Google Drive** — load directly from a shared Drive folder (OAuth 2.0)
- **OpenFDA API** — live medicine data via MCP server
- **Tavily Web Search** — fallback for unknown topics

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Google Gemini API key
- Tavily API key (for web search)
- Google OAuth credentials (`credential.json`) for Drive integration

### Installation

```bash
git clone https://github.com/your-username/agentic-ai-chatbot.git
cd agentic-ai-chatbot

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_gemini_api_key
TAVILY_API_KEY=your_tavily_api_key
OPENAI_API_KEY=your_openai_api_key   # optional, if using OpenAI
```

### Ingest Documents

```bash
# From local file
python -m app.rag.ingest

# From Google Drive folder
python -m app.rag.ingest  # edit ingest.py to set source="google_docs" and folder_id
```

### Start the MCP Server

```bash
python -m app.mcp_server.server
# Runs on http://localhost:8001
```

### Start the API Server

```bash
uvicorn main:app --reload
# Runs on http://localhost:8000
```

---

## 📡 API Reference

### Chat

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/chat` | Send a query, get a full response |
| `POST` | `/chat/stream` | Send a query, stream the response |
| `GET` | `/chat/history/{session_id}` | Get conversation history |

### Human-in-the-Loop

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/chat/status/{session_id}` | Check if a session awaits approval |
| `POST` | `/chat/approve/{session_id}` | Approve and resume a pending query |
| `POST` | `/chat/reject/{session_id}` | Reject and return a safe response |

### Request Body

```json
{
  "input": "What are the side effects of ibuprofen?",
  "session_id": "optional-uuid-string"
}
```

### Response Body

```json
{
  "output": "Ibuprofen may cause...",
  "intent": "medicine",
  "status": "Ok",
  "message": "Output parsed successfully",
  "session_id": "abc-123"
}
```

---

## 🏗️ Architecture

```
User Query
    │
    ▼
Intent Node (classify: rag / medicine / symptom / general)
    │
    ├──► LLM Node       → General conversation with memory
    ├──► Tool Node       → Symptom checker (structured output)
    ├──► MCP Node ──────► [HUMAN APPROVAL REQUIRED] ──► OpenFDA API
    └──► RAG Node
              │
              ▼
         RAG Sub-Graph
         ┌─────────────────────────────────────┐
         │  Query Transform → Should Retrieve?  │
         │       ↓ yes              ↓ no        │
         │  Multi-Query Retrieval   Generate    │
         │       ↓                             │
         │  Reranking → Grade Docs             │
         │       ↓ relevant   ↓ none           │
         │  Generate Answer   Web Search       │
         │       ↓                ↓            │
         │  Hallucination Grader               │
         │  score ≥ 0.7 → done                 │
         │  score < 0.7 → retry (max 3×)       │
         └─────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| API Framework | FastAPI |
| Agent Orchestration | LangGraph |
| LLM | Google Gemini 2.5 Flash Lite |
| Embeddings | Google `gemini-embedding-001` |
| Vector Store | Chroma |
| MCP Server | FastMCP (SSE transport) |
| Web Search | Tavily |
| Document Source | Google Drive (OAuth 2.0) |
| Memory | JSON file store (per session) |

---

## 📝 Notes

- Session memory is stored as JSON files under `data/chat_memory/`. For production, replace with a persistent database.
- The `MemorySaver` checkpointer is in-memory; LangGraph state is lost on restart. Use `PostgresSaver` or `SqliteSaver` for persistence.
- The MCP server must be running before starting the API server.
- Google Drive OAuth token is cached at `token.json` after the first login.
