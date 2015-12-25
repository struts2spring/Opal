

from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func,\
    Column, Integer, String, Column, Integer, String, create_engine, create_engine

from sqlalchemy.ext.declarative import declarative_base, declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker
from src.dao.Book import Base, Book
from src.dao.Author import Author



class AuthorBookLink(Base):
    """A AuthorBookLink class is an entity having database table. This class is for many to many association between Author and Book."""

    __tablename__ = 'author_book_link'
    id = Column(Integer, primary_key=True)
    authorId = Column('book_id', Integer, ForeignKey('author.id'))
    bookId = Column('author_id', Integer, ForeignKey('book.id'))
    extra_data = Column(String(256))
    author = relationship(Author, backref=backref("book_assoc", cascade="all, delete-orphan"))
    book = relationship(Book, backref=backref("book_assoc", cascade="all, delete-orphan"))