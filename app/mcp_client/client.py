from langchain_mcp_adapters.client import MultiServerMCPClient


def get_mcp_clients():
    return MultiServerMCPClient({
        "medical-tools": {
            "url": "http://localhost:8001/sse",
            "transport": "sse"
        }
    })