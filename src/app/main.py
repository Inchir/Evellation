from flask import render_template, session
from flask_login import LoginManager

from src.app import create_app
from src.app import db_session

# импортируем модели
from src.app import User

app = create_app()
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(User, user_id)


@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')


@app.route("/my.evellation")
def my_evellation():
    return render_template('my_evellation.html')


if __name__ == "__main__":
    db_session.global_init("database/users.db")
    app.run("127.0.0.1", 8000, debug=True)
