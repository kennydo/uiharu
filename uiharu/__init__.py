import logging

from flask import Flask

from uiharu.models import db


log = logging.getLogger(__name__)


def create_app(config_dict):
    app = Flask(__name__, static_folder=None)
    app.config.update(**config_dict)

    db.init_app(app)

    from uiharu.api.views import api as api_blueprint
    from uiharu.weather.views import weather as weather_blueprint

    app.register_blueprint(api_blueprint, url_prefix='/api/v1')
    app.register_blueprint(weather_blueprint)

    log.info(app.url_map)

    return app
