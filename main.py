from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv
from database import engine
from models import Base

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize FastAPI app
app = FastAPI()

# Ensure database tables are created
Base.metadata.create_all(bind=engine)

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.post("/chat")
def chat(request: ChatRequest):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": request.message}]
    )
    return {"response": response.choices[0].message["content"]}

@app.get("/orders")
def get_orders():
    return {"order_status": "Your order is being processed."}

@app.post("/returns")
def process_return():
    return {"return_status": "Your return request has been received."}
