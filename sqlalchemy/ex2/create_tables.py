from models import Base,User,Comment
from main import engine

Base.metadata.create_all(bind=engine)