from sqlalchemy.orm import Session
from sqlalchemy import create_engine,text

engine = create_engine('sqlite:///sample.db',echo=True)

session = Session(bind=engine)