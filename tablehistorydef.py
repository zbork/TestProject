from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

history_engine = create_engine('sqlite:///history.db', echo=True)
Base = declarative_base()
 

class Entry(Base):
	__tablename__ = "history"

	id = Column(Integer, primary_key=True)
	username = Column(String)
	number = Column(Integer)


	def __init__(self, username, number):
		self.username = username
		self.number = number
 
# create tables
Base.metadata.create_all(history_engine)