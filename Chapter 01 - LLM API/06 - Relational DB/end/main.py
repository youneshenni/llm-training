from db.main import engine, Base
from db.models import User, Conversation, Message
from sqlalchemy.orm import Session
from llm import conversationLoop

username = input("Please enter your username: ")
with Session(engine) as session:
    user = session.query(User).filter_by(username=username).first()
    if not user:
        print(f"User '{username}' not found. Creating it now...")
        user = User(name=username, username=username, password="password")
        session.add(user)
        print(f"User '{username}' created: {user}")
    else:
        print(f"User '{username}' found: {user}")
    print(f"User '{username}' is now ready to use the application.")
    conversation_name = input("Please enter a name for your conversation: ")
    conversation = Conversation(name=conversation_name, user_id=user.id, tokens=0)
    session.add(conversation)
    conversationLoop(user, conversation, session)
    total_tokens = sum(message.tokens for message in session.query(Message).filter_by(conversation_id=conversation.id).all())
    conversation.tokens = total_tokens
    session.commit()

