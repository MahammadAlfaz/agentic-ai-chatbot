

from app.tools.tools import get_tools


tools=get_tools()

for tool in tools:
    print(tool.name)
    print(tool.invoke("fever and cough"))

    