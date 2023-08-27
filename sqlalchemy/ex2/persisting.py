from models import User, Comment
from main import session

user1 = User(
    username = 'Hasan',
    email_address = 'hasanyucel34@gmail.com',
    comments = [
        Comment(text="Hello World"),
        Comment(text="Test")
    ]
)

user2 = User(
    username = 'Kamil',
    email_address = 'kamil@gmail.com',
    comments = [
        Comment(text="Hello Türkiye"),
        Comment(text="Test 2")
    ]
)

user3 = User(
    username = 'Elif',
    email_address = 'elif@gmail.com',
    comments = [
        Comment(text="Hello Angola"),
        Comment(text="Test 3")
    ]
)

session.add_all([user1,user2,user3])
session.commit()