import os

class Config:
    SECRET_KEY='vexus'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://victor:12345@localhost/blogpost1'
    UPLOADED_PHOTOS_DEST = 'app/static/photos'
    BASE_URL='http://quotes.stormconsultancy.co.uk/random.json'

    # email configurations
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    SUBJECT_PREFIX = 'PersBlog'

class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://victor:12345@localhost/blogpost_test1'


class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://victor:12345@localhost/blogpost1'
    DEBUG = True

config_options = {
    'development': DevConfig,
    'production': ProdConfig,
}
