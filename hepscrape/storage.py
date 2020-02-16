
	
import os
import sys

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
 
class HepPub(Base):
    __tablename__ = 'publication'
    
    id = Column(String(50), primary_key=True)
    title = Column(String(250), nullable=True)
    collaboration = Column(String(25), nullable=True)
    journal =  Column(String(50), nullable=True)
    inspire =  Column(String(50), nullable=True)
    year = Column(Integer, nullable=True)

    def is_complete(self):
        for attribute in filter(lambda x: not x.startswith("_"), dir(self)):
            if not getattr(self, attribute):
                return False

        return True