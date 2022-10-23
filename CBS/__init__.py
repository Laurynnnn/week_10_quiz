import os
from flask import Flask
from .config import app_config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
# import sqlite3 as sql

# db variable initialization
db = SQLAlchemy()

# Marshmallow initialization
ma = Marshmallow()

# initialize migrate 
migrate = Migrate()

TEMPLATES_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Templates')


def create_app():
    cbs_app = Flask(__name__, template_folder=TEMPLATES_FOLDER)
    cbs_app.config.from_object(app_config['development'])
    db.init_app(cbs_app)
    ma.init_app(cbs_app)
    migrate.init_app(cbs_app, db)

    from .views.cbs_news import cbsviews

    cbs_app.register_blueprint(cbsviews)

    return cbs_app
