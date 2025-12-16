from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = f'postgresql+psycopg2://{os.getenv('DATABASE_USER')}:{os.getenv('DATABASE_PASSWORD')}@{os.getenv('DATABASE_HOST')}/{os.getenv('DATABASE_NAME')}'

engine = create_engine(DATABASE_URL)

Session = sessionmaker(bind=engine,autoflush=False,autocommit=False)

Base = declarative_base()

#Yield DB session
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()