from app import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text, DateTime, Float, ForeignKey
import sqlalchemy as sa
from datetime import datetime, timezone

class Base(db.Model):
    __abstract__ = True
    def now_utc(self):
        return datetime.now(timezone.utc)

class Category(Base):
    __tablename__ = 'categories'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    products: Mapped[list["Product"]] = relationship(back_populates="category")

class Product(Base):
    __tablename__ = 'products'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    description: Mapped[str] = mapped_column(Text, nullable=True)
    price: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)

    category_id: Mapped[int] = mapped_column(Integer, ForeignKey('categories.id'), nullable=True)
    category: Mapped["Category"] = relationship(back_populates="products")
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey('categories.id'), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=sa.func.now())

    category: Mapped["Category"] = relationship(back_populates="products")
    
class Post(Base):
    __tablename__ = 'post'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    posted: Mapped[datetime] = mapped_column(DateTime, default=sa.func.now())
    author: Mapped[str] = mapped_column(String(100), nullable=True)