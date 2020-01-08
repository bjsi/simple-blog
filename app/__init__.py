from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from elasticsearch import Elasticsearch


db = SQLAlchemy()


def create_app():
    """ Application Factory Style """

    app = Flask(__name__)
    app.config.from_object('config.Config')
    db.init_app(app)
    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
            if app.config['ELASTICSEARCH_URL'] else None

    with app.app_context():
        from . import models
        from . import views
        db.create_all()

        return app
