from fastapi import FastAPI, Request, HTTPException
from configparser import ConfigParser
from src.factory import get_git_service
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load configuration from config.ini
config = ConfigParser()
config.read("config.ini")

# Initialize FastAPI application
app = FastAPI()

@app.get("/")
def read_root():
    """
    Root endpoint. Returns a simple message.
    """
    return {"Not Found."}

@app.post("/review")
async def reviewPR(request: Request):
    """
    Endpoint to handle pull request review.
    Supports only PR creation events.
    """
    try:
        # Parse the incoming request data
        request_data = await request.json()
        service = get_git_service(config, request, request_data)

        # Handle PR creation event
        if request_data['action'] == 'opened':
            response = service.pr_created()
        else:
            response = "Only PR Creation is supported at this moment."
        return response
    except ValueError as e:
        # Handle invalid input
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(status_code=500, detail="Internal Server Error.")
