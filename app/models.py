from app import db
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Text, DateTime
import sqlalchemy as sa
from datetime import datetime, timezone

class Base(db.Model):
    __abstract__ = True
    
    def now_utc(self):
        return datetime.now(timezone.utc)

class Post(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    
    content: Mapped[str] = mapped_column(Text, nullable=False)
    
    posted: Mapped[datetime] = mapped_column(DateTime, default=sa.func.now())

    def __repr__(self):
        return f'<Post {self.title}>'