from flask import Flask
from flask_restful import Api
from src.resources.hello_world import HelloWorld, HelloWorld2
from src.resources.available import AvailablePreConfigs
from flask_mongoengine import MongoEngine
from .config import MONGO_SETTINGS


def create_app(is_testing=False):
    """
    Create the Flask app
    """
    app = Flask(__name__)

    if is_testing:
        app.config["TESTING"] = True
        app.config["MONGODB_SETTINGS"] = {
            "host": "mongomock://localhost",
            "db": "measuresoftgram",
        }
    else:
        app.config["MONGODB_SETTINGS"] = MONGO_SETTINGS

    api = Api(app)

    # FIXME: Create routes file
    api.add_resource(HelloWorld, "/hello")

    api.add_resource(HelloWorld2, "/hello-world")

    api.add_resource(AvailablePreConfigs, "/available-pre-configs")

    db = MongoEngine(app)

    return app, api, db
