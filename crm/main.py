from flask import render_template, session
from flask_login import LoginManager

# импортируем модели
from crm.models import User

# импортируем сессию
from crm.models import create_session, global_init

# настройка приложения
from crm.create_app import create_app

app = create_app()
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    with create_session() as db_sess:
        return db_sess.get(User, user_id)


@app.route("/")
@app.route("/index")
def index():
    return render_template('base.html')


if __name__ == "__main__":
    global_init("database/users.db")
    print("* Running on http://127.0.0.1:8000")
    app.run("127.0.0.1", 8000, debug=False)
