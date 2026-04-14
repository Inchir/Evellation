from flask_login import current_user

# сессия
from . import db_session

# модель
from . import Account, User

# константы
PREFIX = "evellation"


# формируем путь к шиблонам
def get_templates_name(file_name):
    return f"{PREFIX}/{file_name}"


def create_account(form) -> Account:
    account = Account()
    account.name = form.name.data
    account.user_id = current_user.id
    account.subdomain = form.subdomain.data
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
