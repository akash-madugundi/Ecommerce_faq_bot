from fastapi import FastAPI, Request
from pydantic import BaseModel
import requests
import os

app = FastAPI()

DIALOGFLOW_PROJECT_ID = os.getenv("DIALOGFLOW_PROJECT_ID")
DIALOGFLOW_ACCESS_TOKEN = os.getenv("DIALOGFLOW_ACCESS_TOKEN")

class QueryRequest(BaseModel):
    query: str

def send_query_to_dialogflow(query: str):
    url = f"https://dialogflow.googleapis.com/v2/projects/{DIALOGFLOW_PROJECT_ID}/agent/sessions/12345:detectIntent"
    
    headers = {
        "Authorization": f"Bearer {DIALOGFLOW_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "queryInput": {
            "text": {
                "text": query,
                "languageCode": "en"
            }
        }
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.json()

@app.post("/chat")
async def chat(request: QueryRequest):
    query = request.query
    dialogflow_response = send_query_to_dialogflow(query)
    response_text = dialogflow_response.get("queryResult", {}).get("fulfillmentText", "Sorry, I didn't understand that.")
    
    return {"response": response_text}
