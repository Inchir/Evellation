from flask import Blueprint, url_for

from flask import render_template, session, redirect
from flask_login import login_user, logout_user

# формы
from . import LoginForm, RegisterForm

# сессия
from . import db_session

# модель
from . import User

# Create a blueprint instance
user_bp = Blueprint('user', __name__)


@user_bp.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()

        if user and user.check_password(str(form.password.data)):
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for("my_evellation"))
        return render_template('sign_in.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('sign_in.html', form=form)


@user_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("index"))


@user_bp.route("/sign_up", methods=['GET', 'POST'])
def sign_up():
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('sign_up.html',
                                   form=form,
                                   message="Пользователь с такой почтой уже есть")
        # создаем пользовател
        user = create_user(form)

        # сохраняем
        db_sess.add(user)
        db_sess.commit()

        # логиним
        login_user(user)

        return redirect(url_for('my_evellation'))

    return render_template('sign_up.html', form=form)


def create_user(form):
    user = User()
    user.name = form.name.data
    user.email = form.email.data
    user.set_password(form.password.data)
    return user
