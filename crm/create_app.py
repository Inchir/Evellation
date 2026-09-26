from flask import Flask

import logging

from crm.routes import blueprints

from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY = os.environ.get("SECRET_KEY")


def setup_html_logger():
    """Настройка вывода логов работы html"""
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
    app.config['SECRET_KEY'] = SECRET_KEY
    setup_html_logger()  # настраиваем вывод логгеров

    # Register blueprint
    for blueprint in blueprints:
        app.register_blueprint(blueprint, url_prefix='/')

    return app
