from flask import Flask
from routes import blueprints

import logging

# импортируем сессию
from src.models import db_session
# импортируем модели
from src.models.users import User

# формы
from src.app.forms import EventsForm


def setup_html_logger():
    """настройка вывода логов работы html"""
    werkzeug_logger = logging.getLogger("werkzeug")

    handler = logging.FileHandler("./http.log", encoding="UTF-8")
    handler.setFormatter(
        logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))

    werkzeug_logger.handlers.clear()
    werkzeug_logger.addHandler(handler)
    werkzeug_logger.setLevel(logging.INFO)
    werkzeug_logger.propagate = False


def create_app():
    # устанавливаем данные для формы

    app = Flask(__name__)
    app.config['SECRET_KEY'] = '1231231231'
    setup_html_logger()  # настраиваем вывод логгеров

    # Register blueprint
    for blueprint in blueprints:
        app.register_blueprint(blueprint, url_prefix='/')

    return app
