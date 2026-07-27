from typing import List
from typing import Optional
from sqlalchemy import Enum, ForeignKey
from sqlalchemy import String, Text
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    username: Mapped[str] = mapped_column(String(30), unique=True)
    password: Mapped[str] = mapped_column(String(30))
    messages: Mapped[List["Message"]] = relationship(back_populates="user")
    conversations: Mapped[List["Conversation"]] = relationship(back_populates="user")
    quota: Mapped[Optional["Quota"]] = relationship(back_populates="user", uselist=False)
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, username={self.username!r})"

class Message(Base):
    __tablename__ = "message"
    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(Text)
    tokens: Mapped[int] = mapped_column()
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("user.id"))
    user: Mapped[Optional["User"]] = relationship(back_populates="messages")
    role: Mapped[str] = mapped_column(Enum("user", "assistant", name="role_enum"))
    conversation_id: Mapped[Optional[int]] = mapped_column(ForeignKey("conversation.id"))
    conversation: Mapped[Optional["Conversation"]] = relationship(back_populates="messages")
    def __repr__(self) -> str:
        return f"Message(id={self.id!r}, content={self.content!r}, tokens={self.tokens!r}, user_id={self.user_id!r}, role={self.role!r})"
    
class Conversation(Base):
    __tablename__ = "conversation"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("user.id"))
    user: Mapped[Optional["User"]] = relationship(back_populates="conversations")
    name: Mapped[str] = mapped_column(String(30))
    messages: Mapped[List["Message"]] = relationship(back_populates="conversation")
    tokens: Mapped[int] = mapped_column()
    def __repr__(self) -> str:
        return f"Conversation(id={self.id!r}, name={self.name!r})"
    
class Quota(Base):
    __tablename__ = "quota"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("user.id"))
    user: Mapped[Optional["User"]] = relationship(back_populates="quota")
    tokens: Mapped[int] = mapped_column()
    def __repr__(self) -> str:
        return f"Quota(id={self.id!r}, tokens={self.tokens!r})"