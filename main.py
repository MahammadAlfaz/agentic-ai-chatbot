from fastapi import FastAPI

from app.api.routes import router


app=FastAPI(
    title="medical assistant",
    description="medical chatbot using langchain and langgraph",
    version="1.0"
)

app.include_router(router)
@app.get("/")
def root():
    return {"message":"working "}


@app.get("/health")
def health():
    return {"status":"ok"}