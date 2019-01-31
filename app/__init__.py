from flask import Flask
from werkzeug.exceptions import HTTPException
from peewee import MySQLDatabase

from app.misc.log import log
from app.models import BaseModel


def register_extensions(flask_app: Flask):
    from app import extensions

    extensions.db = MySQLDatabase(**flask_app.config['DB_SETTING'])


def register_views(flask_app: Flask):
    from app.views import route

    route(flask_app)


def register_hooks(flask_app: Flask):
    from app.hooks.error import broad_exception_handler, http_exception_handler
    from app.hooks.request_context import after_request

    flask_app.after_request(after_request)
    flask_app.register_error_handler(HTTPException, http_exception_handler)
    flask_app.register_error_handler(Exception, broad_exception_handler)


def create_tables():
    from app import extensions

    from app.models import BaseModel
    from app.models import post, user

    extensions.db.create_tables(BaseModel.__subclasses__())


def create_app(*config_cls) -> Flask:
    log(message='Flask application initialized with {}'.format(', '.join([config.__name__ for config in config_cls])),
        keyword='INFO')

    flask_app = Flask(__name__)

    for config in config_cls:
        flask_app.config.from_object(config)

    register_extensions(flask_app)
    register_views(flask_app)
    register_hooks(flask_app)
    create_tables()

    return flask_app
