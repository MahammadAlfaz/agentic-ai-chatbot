import asyncio
import json

from app.graph.state import AgentState
from app.llm.llm import get_llm
from app.mcp_client.client import get_mcp_clients



async def _mcp_node_async(state:AgentState):
    user_input=state['input']
    llm=get_llm()

    client=get_mcp_clients()
    tools=await client.get_tools()

    llm_with_tools=llm.bind_tools(tools)

    prompt = f"""
        You are a medical assistant.
        Use the available tools to find real medicine information.
        
        User query: {user_input}
        """
    result = await llm_with_tools.ainvoke(prompt)

    if result.tool_calls:
        tool_call=result.tool_calls[0]
        tool_name=tool_call['name']
        tool_args=tool_call['args']

        tool=next(t for t in tools if t.name==tool_name)
        tool_result= await tool.ainvoke(tool_args)
        if isinstance(tool_result, list):
         content = tool_result[0].get("text", str(tool_result))
        elif isinstance(tool_result, dict):
         content = tool_result
        else:
         content = str(tool_result)

        return {'output':tool_result}
    

    return {"output":content}
def mcp_node(state: AgentState):       
    return asyncio.run(_mcp_node_async(state))