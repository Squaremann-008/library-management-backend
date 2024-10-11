import uuid
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, Enum, DateTime, Text, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    name = Column(String)
    address = Column(String)
    contact_info = Column(String)
    role = Column(Enum("user", "admin", name="user_role"), default="user")
    is_active = Column(Boolean, default=True)
    mfa_secret = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

class Book(Base):
    __tablename__ = "books"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String)
    author = Column(String)
    genre = Column(String)
    description = Column(Text)
    total_copies = Column(Integer)
    available_copies = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

class Borrowing(Base):
    __tablename__ = "borrowings"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    book_id = Column(UUID(as_uuid=True), ForeignKey('books.id'))
    borrowed_at = Column(DateTime, default=datetime.utcnow)
    due_date = Column(DateTime)
    returned_at = Column(DateTime, nullable=True)
    is_renewed = Column(Boolean, default=False)
    overdue = Column(Boolean, default=False)
    fine_amount = Column(DECIMAL, default=0)

class Reservation(Base):
    __tablename__ = "reservations"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    book_id = Column(UUID(as_uuid=True), ForeignKey('books.id'))
    reserved_at = Column(DateTime, default=datetime.utcnow)
    status = Column(Enum("active", "cancelled", "completed", name="reservation_status"), default="active")

class Fine(Base):
    __tablename__ = "fines"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    borrowing_id = Column(UUID(as_uuid=True), ForeignKey('borrowings.id'))
    amount = Column(DECIMAL)
    paid = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    paid_at = Column(DateTime, nullable=True)
