#FastAPI lets python receive requests from node.js
from fastapi import FastAPI 

#creates a form template for json data from node.js so that python can process this data
from pydantic import BaseModel

#imports the process_query function from main.py. api.py receives requests from node calls the below function from main.py which process and return the results to api.p
from main import process_query

import os #access env 
from dotenv import load_dotenv #imports the enironment confuguration variables
load_dotenv() #loads the env file

app = FastAPI() #creates a python web framework

#create a base model that exactly matches the node.js form

#This class inherits from basemodel which allows the validation automatically without needing to write the code. LIke if the fields are automatically validated, check if fields are missing or they are correct type and reject bad requests.
class QueryRequest(BaseModel):
    query: str
    customer_name: str
    customer_email: str
    provider: str = "groq"

#app.post is a decorator function. It receives request from node.js and matches the query request template
@app.post("/process")
def process(request: QueryRequest):
    #calls process_query from main.py with data from Node.js
    result = process_query(
        query = request.query, #message field from json body
        customer_name= request.customer_name, #customer name from node.js 
        customer_email=request.customer_email #customer email from node.js 
    )
    return result

@app.get("/tickets")
def get_tickets():
    from tools.database_tool import get_all_tickets
    tickets = get_all_tickets()
    return tickets


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)