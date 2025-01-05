
import os
import dotenv

dotenv.load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///inventory.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret')
    USER_NAME = os.getenv('USER_NAME', 'rootxx')
    USER_PASSWORD = os.getenv('USER_PASSWORD', 'rootpasswordxx')  