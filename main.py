from fastapi import FastAPI, Request, HTTPException
from configparser import ConfigParser
from gitService import GitHubService, GiteaService
import json
from util import getGitandEventType

config = ConfigParser()
config.read("config.ini")

app = FastAPI()

@app.get("/")
def read_root():
    return {"Not Found."}

@app.post("/review")
async def reviewPR(request: Request):
    try:
        git, eventType = getGitandEventType(request)
        if (eventType != 'pull_request'):
            return "Not a pull request event"
        requestData = await request.json()
        if git == 'GitHub':
            requestData = json.loads(requestData["payload"])
            service = GitHubService(config, requestData)
        else:
            service = GiteaService(config, requestData)
        if (requestData['action'] == 'opened'):
            response = service.prCreated()
        else:
            response = "Only PR Creation is supported at this moment."
        return response
    except:
        raise HTTPException(status_code=500, detail="Internal Server Error.")
