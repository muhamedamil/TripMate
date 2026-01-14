import os
import sys
from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import uvicorn

load_dotenv()

from agent.agentic_workflow import GraphBuilder
from logger.logger import logger
from exception.exception_handling import TripMateException

app = FastAPI(title="Trip Mate")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def read_root():
    """
    Serve the frontend application.
    """
    logger.info("Serving index.html")
    if not os.path.exists("static/index.html"):
        logger.error("static/index.html not found!")
        return JSONResponse(
            status_code=404, content={"error": "Frontend files missing"}
        )
    return FileResponse("static/index.html")


@app.get("/health")
async def health_check():
    return {"status": "ok"}


class QueryResponse(BaseModel):
    """
    Data model for the query response.
    """
    query: str


@app.post("/query")
async def query_travel_agent(query: QueryResponse):
    """
    FastAPI endpoint to query the travel agent.

    Args:
        query (QueryResponse): The user's query wrapped in a Pydantic model.

    Returns:
        JSONResponse: A JSON object containing the answer or an error message.
    """
    try:
        logger.info(f"Received query: {query.query}")
        graph = GraphBuilder(model_provider="groq")
        react_app = graph()

        messages = {"messages": [query.query]}

        logger.info("Invoking travel agent graph")
        output = react_app.invoke(messages)

        # if result is dict with messages:
        if isinstance(output, dict) and "messages" in output:
            final_output = output["messages"][
                -1
            ].content  # to retrieve the latest AI response
        else:
            final_output = str(output)

        logger.info("Query processed successfully")
        return {"answer": final_output}
    except Exception as e:
        error = TripMateException(e, sys)
        logger.error(error.error_message)
        return JSONResponse(status_code=500, content={"error": str(error)})


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)
