import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-for-testing'
    MONGO_URI = os.environ.get('MONGO_URI')
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
