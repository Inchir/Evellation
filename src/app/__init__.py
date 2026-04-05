from flask import Flask
from routes import blueprints

# импортируем сессию
from src.models import db_session
# импортируем модели
from src.models.users import User


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '1231231231'


    # Register blueprint
    for blueprint in blueprints:
        app.register_blueprint(blueprint, url_prefix='/')

    return app
