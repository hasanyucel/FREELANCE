from sqlalchemy import create_engine
from sqlalchemy import Column,String,Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///sqlalchemy.sqlite',echo=True)

base = declarative_base()

#Tablonun ve veritabanının oluşturulması için çalıştırılması yeterlidir.

class transactions (base):

    __tablename__ = 'transations'

    transactions_id = Column(Integer,primary_key=True)
    date = Column(String)
    item_id = Column(Integer)
    price = Column(Integer)

    def __init__(self,transactions_id,date,item_id,price):
        self.transactions_id = transactions_id
        self.date = date
        self.item_id = item_id
        self.price = price

base.metadata.create_all(engine)