from main import session
from models import User,Comment
from sqlalchemy import select

#statement = select(User).where(User.username.in_(['Hasan','Kamil']))
#result = session.scalars(statement)
#for user in result:
#    print(user)

#users = session.query(User).all()
#for user in users:
#    print(user)

#hasan = session.query(User).filter_by(username = 'Hasan').first
#print(hasan)

statement = select(Comment).join(Comment.user).where(
    User.username == 'Hasan'
).where(
    Comment.text == 'Hello World'
)

result = session.scalars(statement)
print(result)