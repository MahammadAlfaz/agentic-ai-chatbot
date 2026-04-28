

import httpx
from mcp.server import FastMCP


mcp=FastMCP("medicine-tools",port=8001)

async def get_medicine_info(medicine_name:str)->str:
    """Fetch real medicine information from OpenFDA database."""
    url=f"https://api.fda.gov/drug/label.json?search={medicine_name}&limit=1"
    async with httpx.AsyncClient() as client:
        response=await client.get(url)

        if response.status_code != 200:
            return f"Cold not find the information for {medicine_name}"
        
        data=response.json()
        print(data)
        result=data['results'][0]

        info={
            "name":medicine_name,
            "purpose":result.get("purpose",['Not available'])[0],
            "warnings":result.get("warnings", ["Not available"])[0],
            "dosage": result.get("dosage_and_administration", ["Not available"])[0]
        }
        return str(info)


if __name__=="__main__":
    mcp.run(transport="sse")

