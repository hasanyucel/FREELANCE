import db
from sqlalchemy.orm import sessionmaker
import random

Session = sessionmaker(bind=db.engine)
session = Session()

for i in range (20,30):
    item_id = random.randint(0,1000)
    price = random.randint(20,50)

    tr = db.transactions(i,'27/08/2023',item_id,price)
    session.add(tr)

session.commit()