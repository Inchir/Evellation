from flask import Blueprint, url_for
from flask import render_template, redirect
from flask_login import current_user

# формы
from . import AccountForm, TokenForm

# сессия
from . import db_session

# модель
from . import Account, User

# Create a blueprint instance
evellation_bp = Blueprint('evellation', __name__)

# константы
PREFIX = "evellation"


# формируем путь к шиблонам
def get_templates_name(file_name):
    return f"{PREFIX}/{file_name}"


def create_account(form) -> Account:
    account = Account()
    account.name = form.name.data
    account.user_id = current_user.id
    return account


def get_accounts(user_id) -> list:
    db_sess = db_session.create_session()
    return [account for account in db_sess.query(Account).filter(Account.user_id == user_id).all()]


def get_account(account_id) -> Account:
    db_sess = db_session.create_session()
    return db_sess.query(Account).filter(Account.id == account_id).first()

def get_user(user_id) -> User:
    db_sess = db_session.create_session()
    return db_sess.query(User).filter(User.id == user_id).first()


@evellation_bp.route('/my.evellation')
def my_evellation():
    return render_template(get_templates_name("base.html"), accounts=get_accounts(current_user.id))


@evellation_bp.route('/my.evellation/<account_id>')
def my_evellation_account(account_id):
    account = get_account(account_id)
    if not account or account.user_id != current_user.id:
        return redirect('/my.evellation')
    return render_template(get_templates_name("account.html"),
                           accounts=get_accounts(current_user.id), account=account)


@evellation_bp.route('/my.evellation/token', methods=['GET', 'POST'])
def enter_token():
    form = TokenForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()

        #получаем полбзователя
        user = get_user(current_user.id)

        #устонавливаем токен
        user.token = form.token.data

        db_sess.merge(user)
        db_sess.commit()


        return redirect('/my.evellation')

    return render_template(get_templates_name("create_account.html"), form=form)


@evellation_bp.route('/my.evellation/create.account', methods=['GET', 'POST'])
def sign_in():
    form = AccountForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(Account).filter(Account.name == form.name.data).first():
            return render_template(get_templates_name("create_account.html"), form=form,
                                   message="Аккаунт с таким названием уже есть")
        # создаем аккаунт
        account = create_account(form)

        # сохраняем
        db_sess.add(account)
        db_sess.commit()

        return redirect('/my.evellation')

    return render_template(get_templates_name("create_account.html"), form=form)
