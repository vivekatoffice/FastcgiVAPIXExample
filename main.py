from typing import List, Optional
from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://192.168.55.157:8081",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
import requests
import json

vapix_url = "http://192.168.55.176/axis-cgi/apidiscovery.cgi"

headers = {
  'Content-Type': 'application/json'
}

class Payload(BaseModel):
    apiVersion: str
    method: str | None = "getApiList"

@app.post("/apidiscovery/")
async def create_item(request: Request):
    body_from_request = await request.json()
    
    first_val = list(body_from_request.values())[0]
    second_val = list(body_from_request.values())[1]
    payload = json.dumps({
        "apiVersion":first_val,
        "method": second_val
    })
    response = requests.request("POST", vapix_url, headers=headers, data=payload)
    #convert string to  object
    json_object = json.loads(response.text)
    return {"response":json_object}

@app.post('/my_endpoint')
def read_root(request: Request):
    client_host = request.client.host
    return {"client_host": client_host}
