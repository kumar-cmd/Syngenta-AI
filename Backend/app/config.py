import os
from dotenv import load_dotenv
load_dotenv("/home/syngentai/mysite/.env")

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'devkey')
    SECURITY_PASSWORD_SALT = os.getenv('SECURITY_PASSWORD_SALT', 'salt')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///../instance/app.db')
    SECURITY_REGISTERABLE = True
    SECURITY_SEND_REGISTER_EMAIL = False
    SECURITY_TRACKABLE = True
    SECURITY_TOKEN_AUTHENTICATION = True
    SECURITY_TOKEN_AUTHENTICATION_MODE = 'jwt'
    SECURITY_JWT_SECRET = os.getenv('JWT_SECRET', 'anothersecretkey')
    SECURITY_JWT_HEADER_NAME = 'Authorization'
    SECURITY_JWT_HEADER_TYPE = 'Bearer'
    SECURITY_JWT_EXPIRATION_DELTA = 3600
    VECTORDIR = os.getenv('VECTORDIR', 'app/vector_store')
    AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
    BEDROCK_API_KEY = os.getenv('BEDROCK_API_KEY', '')
