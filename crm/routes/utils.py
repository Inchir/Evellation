from flask_login import current_user

# сессия
from crm.models import create_session

# модель
from crm.models import Account, User

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
    with create_session() as db_sess:
        return [account for account in db_sess.query(Account).filter(Account.user_id == user_id).all()]


def get_account(account_id) -> Account:
    with create_session() as db_sess:
        return db_sess.query(Account).filter(Account.id == account_id).first()


def get_user(user_id) -> User:
    with create_session() as db_sess:
        return db_sess.query(User).filter(User.id == user_id).first()


def set_errors(status_code) -> str | None:
    """Возвращает текст,
    который будет показан пользователю,
    в зависимости от кода ошибки"""
    if status_code == 400:
        return "Переданы некорректные параметры"
    if status_code == 402:
        return "аккаунт не оплачен"
    if status_code == 401:
        return "Неверный субдомен или токен"

    if status_code == 501:
        return "сбой при получении данных"
    if status_code == 202:
        return "Нет сделок за этот период"
    if status_code == 204:
        return "Нет данных такого типа"

    if status_code == 200:
        # все хорошо, сообщение показывать не надо
        return None
    else:
        return "Непредвиденная ошибка"
