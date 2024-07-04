from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import openai
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse


import os
from dotenv import load_dotenv

api_key = os.getenv('OPENAI_API_KEY')


load_dotenv()  # Load environment variables from .env file

app = FastAPI()

# Enable CORS
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://yourfrontenddomain.com",  # Add your frontend domain here
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class OpenAIClient:
    def __init__(self, api_key):
        self.client = openai.OpenAI(api_key=api_key)

    def chat(self, messages):
        completion = self.client.chat.completions.create(
            model="gpt-4o",
            messages=messages
        )
        return completion.choices[0].message.content


class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]

# Initialize the OpenAI client with your API key
openai_client = OpenAIClient(api_key=api_key)

@app.post("/chat/")
async def chat_endpoint(chat_request: ChatRequest):
    try:
        response = openai_client.chat(chat_request.messages)
        return JSONResponse({
            "content": response,
            "role": "assistant"
            })
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
