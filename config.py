import os
from decouple import config

class Config:
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'app/static/videos/inputs')
    OUTPUT_FOLDER = os.path.join(os.getcwd(), 'app/static/videos/outputs')
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # Max 100MB
    MODEL_PATH = os.path.join(os.getcwd(), 'files/model.h5')
    SQLALCHEMY_DATABASE_URI = f"postgresql://{config('PGSQL_USER')}:{config('PGSQL_PASSWORD')}@{config('PGSQL_HOST')}/{config('PGSQL_DATABASE')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = config('SECRET_KEY')


class DevelopmentConfig(Config):
    DEBUG = True

config = {
    'development': DevelopmentConfig,
}
