

import httpx
from mcp.server.fastmcp import FastMCP

from app.mcp_server.schemas import MedicineResponse


mcp=FastMCP("medicine-tools",port=8001)

@mcp.tool()
async def get_medicine_info(medicine_name:str)->dict:
    """Fetch real medicine information from OpenFDA database."""

    brand_to_generics = {
    "dolo": "acetaminophen",      
    "crocin": "acetaminophen",
    "paracetamol": "acetaminophen",  
    "combiflam": "ibuprofen",
    "corex": "codeine",
}
    search_name=medicine_name
    for brand,generics in brand_to_generics.items():
        if brand in medicine_name.lower():
          search_name=generics
          break



    url=f"https://api.fda.gov/drug/label.json?search={search_name}&limit=1"
    async with httpx.AsyncClient() as client:
        response=await client.get(url)

        if response.status_code != 200:
            return {
                "output":f"Cold not find the information for {medicine_name}"
            }
        
        data=response.json()
        result=data.get("results",[])

        if not result:
            return {
                "output":"not found "
            }
        
        result=result[0]
        medicine = MedicineResponse(
                name=medicine_name,
                purpose=result.get("indications_and_usage", ["Not available"])[0][:300],
                dosage=result.get("dosage_and_administration", ["Not available"])[0][:300],
                warnings=result.get("warnings", ["Not available"])[0][:300],
                side_effects=result.get("adverse_reactions", 
                            result.get("do_not_use", ["Not available"]))[0][:300]
            )

        # info={
        #     "name":medicine_name,
        #     "purpose":result.get("purpose",['Not available'])[0],
        #     "warnings":result.get("warnings", ["Not available"])[0],
        #     "dosage": result.get("dosage_and_administration", ["Not available"])[0]
        # }
        return medicine.model_dump()


if __name__=="__main__":
    mcp.run(transport="sse")

