from fastapi import FastAPI


app=FastAPI(
    title="medical assistant",
    description="medical chatbot using langchain and langgraph",
    version="1.0"
)

@app.get("/")
def root():
    return {"message":"working "}


@app.get("/health")
def health():
    return {"status":"ok"}