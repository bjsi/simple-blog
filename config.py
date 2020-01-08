import os


APP_ROOT = os.path.dirname(os.path.realpath(__name__))


class Config:
    FLASK_DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:////' + \
                              os.path.join(APP_ROOT, 'blog.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    ELASTICSEARCH_URL = "http://localhost:9200"
