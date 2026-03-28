from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from core.sql_agent import run_sql_agent
from core.rag_agent import run_rag_agent
from core.intent import classify_intent

app = FastAPI(
    title="AI Business Data Assistant",
    description="Ask questions about your business data in plain English.",
    version="0.1.0",
)


class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    answer: str
    source: str
    sql: str
    


@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):

    question = request.question.strip()

    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    intent = classify_intent(question)

    if intent == "sql":
        result = run_sql_agent(question)
        answer = result["answer"]  
        sql = result["sql"]
        sources = []

    else:
        result = run_rag_agent(question)
        answer = result["answer"]
        sql = ""
        sources = result.get("sources", [])

    return QueryResponse(
        answer=answer,
        source=intent,
        sql=sql,
        sources=sources
    )


@app.get("/health")
async def health():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)