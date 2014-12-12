from connection import Base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy import ForeignKey


class Page(Base):
    __tablename__ = "pages"

    id = Column(Integer, primary_key=True)
    url = Column(String)
    title = Column(String)
    description = Column(String)
    points = Column(Integer)

    website_id = Column(Integer, ForeignKey("websites.id"))
    website = relationship("Website", backref="pages")


class Website(Base):
    __tablename__ = "websites"

    id = Column(Integer, primary_key=True)
    url = Column(String)
    Title = Column(String)
    Domain = Column(String)
    page_count = Column(Integer)
    html_version = Column(Float)


class Keyword(Base):
    __tablename__ = "keywords"

    id = Column(Integer, primary_key=True)
    word = Column(String)

engine = create_engine("sqlite:///pages.db")
Base.metadata.create_all(engine)
