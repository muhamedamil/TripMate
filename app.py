import os
from fastapi import FastAPI
from pydantic import BaseModel

from agent.agentic_workflow import GraphBuilder
from fastapi.responses import JSONResponse

app = FastAPI(title="Trip Mate")

class QueryResponse(BaseModel):
    query: str

@app.post("/query")
async def query_travel_agent(query:QueryResponse):
    try: 
        print(query)
        graph = GraphBuilder(model_provider="groq")
        react_app = graph()
        
        #Assuming request is a pydantic object
        messages = {"messages":[query.question]}
        
        output = react_app.invoke(messages)
        
        #if result is dict with messages:
        if isinstance(output,dict) and messages in output:
            final_output = output["messages"][-1].content # to retreive the latest AI response
        else:
            final_output = str(output)
        return {"answer": final_output}
    except Exception as e :
        return JSONResponse(status_code=500, content={"error":str(e)})
    