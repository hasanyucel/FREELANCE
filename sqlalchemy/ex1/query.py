import db
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=db.engine)
session = Session()

#for s in session.query(db.transactions).all():
#    print(s.transactions_id,s.price)


for s in session.query(db.transactions).filter(db.transactions.price>40):
    print(s.transactions_id,s.price)