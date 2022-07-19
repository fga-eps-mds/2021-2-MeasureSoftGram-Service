from flask import Flask
from flask_restful import Api
from _src.resources.available import AvailablePreConfigs
from _src.resources.pre_config import PreConfigs
from _src.resources.import_metrics import ImportMetrics
from _src.resources.analysis import Analysis
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
    api.add_resource(AvailablePreConfigs, "/available-pre-configs")

    api.add_resource(ImportMetrics, "/import-metrics")

    api.add_resource(PreConfigs, "/pre-configs", "/pre-configs/<string:pre_config_id>")

    api.add_resource(Analysis, "/analysis")

    db = MongoEngine(app)

    return app, api, db
