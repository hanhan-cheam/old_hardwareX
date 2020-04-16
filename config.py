import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    SECRET =  os.getenv('SECRET')
    if os.getenv('FLASK_ENV') == 'development':
        SQLALCHEMY_DATABASE_URI = 'postgresql://' + os.getenv('DEV_DB_USER') + ":" + os.getenv('DEV_DB_PASSWORD') + "@" + os.getenv('DEV_DB_HOST') + ":" + os.getenv('DEV_DB_PORT') + "/" + os.getenv('DEV_DB_NAME')
    elif os.getenv('FLASK_ENV') == 'production':
        SQLALCHEMY_DATABASE_URI = 'postgresql://' + os.getenv('PROD_DB_USER') + ":" + os.getenv('PROD_DB_PASSWORD') + "@" + os.getenv('PROD_DB_HOST') + ":" + os.getenv('PROD_DB_PORT') + "/" + os.getenv('PROD_DB_NAME')
    elif os.getenv('FLASK_ENV') == 'testing':
        SQLALCHEMY_DATABASE_URI = 'postgresql://' + os.getenv('TEST_DB_USER') + ":" + os.getenv('TEST_DB_PASSWORD') + "@" + os.getenv('TEST_DB_HOST') + ":" + os.getenv('TEST_DB_PORT') + "/" + os.getenv('TEST_DB_NAME')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
    SQLALCHEMY_ECHO = 0