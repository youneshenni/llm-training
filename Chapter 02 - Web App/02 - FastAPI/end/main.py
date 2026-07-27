from fastapi import FastAPI
from db.main import engine
from db.models import Conversation, Message
from sqlalchemy.orm import Session
from fastapi.staticfiles import StaticFiles

app = FastAPI()



@app.get("/api/conversation")
async def get_conversations():
    with Session(engine) as session:
        conversations = session.query(Conversation).all()
        return conversations
@app.get("/api/conversation/{conversation_id}")
async def get_conversation(conversation_id: int):
    with Session(engine) as session:
        messages = session.query(Message).filter_by(conversation_id=conversation_id).all()
        if messages:
            return messages
        else:
            return {"error": "Conversation not found"}
app.mount("/", StaticFiles(directory="static"), name="static")