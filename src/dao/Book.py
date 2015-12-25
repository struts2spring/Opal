
from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func, \
    Column, Integer, String, Column, Integer, String, create_engine, create_engine

from sqlalchemy.ext.declarative import declarative_base, declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.sql.schema import UniqueConstraint

Base = declarative_base()
engine = create_engine('sqlite:///better_calibre.sqlite')


class Book(Base):
    __tablename__ = 'book'
    """A Book class is an entity having database table."""
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True, autoincrement=True)
    bookName = Column('book_name', String(46), nullable=False)  # bookName
    subTitle = Column('sub_title', String)  # Title
    isbn_10 = Column(String)  # isbn_10
    isbn_13 = Column(String,unique=True)  # isbn_13
    series = Column(String)  # series
    dimension = Column(String)  # dimension
    customerReview = Column('customer_review', String)  # customerReview
    bookDescription = Column('book_description', String)  # bookDescription
    editionNo = Column('edition_no', String)  # editionNo
    publisher = Column(String)  # publisher
    bookFormat = Column("book_format", String)  # bookFormat
    fileSize = Column('file_size', String)  # fileSize
    numberOfPages = Column('number_of_pages', String)  # numberOfPages
    inLanguage = Column('in_language', String)  # inLanguage
    publishedOn = Column('published_on', DateTime, default=func.now())
    hasCover = Column('has_cover', String)  # hasCover
    hasCode = Column('has_code', String)  # hasCode
    bookPath = Column('book_path', String)  # bookPath
    rating = Column('rating', String)  # rating
    uuid = Column('uuid', String)  # uuid
    createdOn = Column('created_on', DateTime, default=func.now())
    authors = relationship(
        'Author',
        secondary='author_book_link', lazy='joined', cascade="all"
    )


#     __table_args__ = (UniqueConstraint('isbn_13', 'location_code', name='_customer_location_uc'),)
