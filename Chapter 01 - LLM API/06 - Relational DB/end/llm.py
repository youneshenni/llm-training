import anthropic
import json
from sqlalchemy.orm import Session
from db.models import Conversation, Message, User

client = anthropic.Anthropic()

def conversationLoop(user: User, conversation: Conversation, session:Session):
    dbMessages = session.query(Message).filter_by(conversation_id=conversation.id).all()
    messages = list(map(lambda m: {"role": m.role, "content": m.content}, dbMessages))
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        message = client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=1000,
            messages=messages + [{"role": "user", "content": user_input}]
        )
        newMessage = Message(content=user_input, role="user", user_id=user.id, conversation_id=conversation.id, tokens=message.usage.input_tokens)
        session.add(newMessage)
        for block in message.content:
                    if block.type == "text":
                        newResponse = Message(content=block.text, role="assistant", user_id=user.id, conversation_id=conversation.id, tokens=message.usage.output_tokens)
                        session.add(newResponse)
                        print(f"Claude: {block.text}")
                        

       
            