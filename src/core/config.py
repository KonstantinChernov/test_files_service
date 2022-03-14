import os


class Config:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    SECRET_KEY = os.getenv('SECRET_KEY', 'lol')

    DEBUG = False
    TESTING = False

    POSTGRES_DB = os.getenv('POSTGRES_DB', 'users_database')
    POSTGRES_USER = os.getenv('POSTGRES_USER', 'postgres')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 1234)
    POSTGRES_HOST = os.getenv('POSTGRES_HOST', '127.0.0.1')
    POSTGRES_PORT = os.getenv('POSTGRES_DB', 5432)

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_PATH = os.path.join(os.path.dirname(BASE_DIR), os.getenv('STORAGE_NAME'))


class DevelopmentBaseConfig(Config):
    DEBUG = True


class ProductionBaseConfig(Config):
    DEBUG = False


class TestBaseConfig(Config):
    DEBUG = False
    TESTING = True
