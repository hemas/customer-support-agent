from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from main import process_query
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Define what the incoming request looks like
class QueryRequest(BaseModel):
    customer_name: str
    customer_email: str
    query: str

# Define what the response looks like
class QueryResponse(BaseModel):
    ticket_id: int
    response: str
    sentiment: str
    intent: str

@app.get("/health")
def health_check():
    """Check if the service is running"""
    return {"status": "ok", "service": "python-agent"}

@app.post("/process")
def process_customer_query(request: QueryRequest):
    """Process a customer query through the AI agent"""
    try:
        result = process_query(
            query=request.query,
            customer_name=request.customer_name,
            customer_email=request.customer_email
        )
        return QueryResponse(
            ticket_id=result['ticket_id'],
            response=result['response'],
            sentiment=result['sentiment'],
            intent=result['intent']
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
