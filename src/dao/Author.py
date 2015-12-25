
from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func,\
    Column, Integer, String, Column, Integer, String, create_engine, create_engine

from sqlalchemy.ext.declarative import declarative_base, declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker
from src.dao.Book import Base,Book

class Author(Base):
    """A Author class is an entity having database table."""

    __tablename__ = 'author'
    id = Column(Integer, primary_key=True)
    authorName = Column('author_name', String(46), nullable=False, autoincrement=True)
    aboutAuthor = Column('about_author', String)
    email = Column(String, unique=True)
    created_on = Column(DateTime, default=func.now())

    books = relationship(
        Book,
        secondary='author_book_link', cascade="save-update, merge, delete"
    )

