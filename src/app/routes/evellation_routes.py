from flask import Blueprint, url_for
from flask import render_template, redirect
from flask_login import current_user

# формы
from . import AccountForm, TokenForm, DataForm

# сессия
from . import db_session

# модель
from . import Account

# импортируем вспомогательные функции
from . import get_templates_name, get_user, get_account, get_accounts, create_account

# Create a blueprint instance
evellation_bp = Blueprint('evellation', __name__)


@evellation_bp.route('/my.evellation')
def my_evellation():
    return render_template(get_templates_name("base.html"), accounts=get_accounts(current_user.id))


@evellation_bp.route('/my.evellation/<account_id>', methods=['GET', 'POST'])
def my_evellation_account(account_id):
    from src.services.amocrm.client import get_data

    from pprint import pprint
    subdomain = 'account2222'  # Ваш поддомен
    access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjlmYTE0ODJkOTEyMDhhOWY0MDM2NmZkZTY2OGM5YjY0MGYzNTU5Y2MwY2UxODA4NzM2YzYyZWZlNGUwMTFjYmY5ZGZhNTQ0NDE1NjIyYzkwIn0.eyJhdWQiOiI3YjQ5MGYxOC0yYmU1LTRhNTUtYTc0ZS0xOTYzYzk2NDFiOTgiLCJqdGkiOiI5ZmExNDgyZDkxMjA4YTlmNDAzNjZmZGU2NjhjOWI2NDBmMzU1OWNjMGNlMTgwODczNmM2MmVmZTRlMDExY2JmOWRmYTU0NDQxNTYyMmM5MCIsImlhdCI6MTc3NTkxMjA0NywibmJmIjoxNzc1OTEyMDQ3LCJleHAiOjE3NzU5MTQ0NDcsInN1YiI6IjEzNjczODcwIiwiZ3JhbnRfdHlwZSI6IiIsImFjY291bnRfaWQiOjAsImJhc2VfZG9tYWluIjpudWxsLCJ2ZXJzaW9uIjoxLCJzY29wZXMiOlsiY2hhdHMiLCJjcm0iLCJtYWlsIiwibm90aWZpY2F0aW9ucyIsInVuc29ydGVkIl0sImhhc2hfdXVpZCI6ImQ4NDhmMGYxLWVjYzMtNDc2NS04YWIzLWExNmZjODVmYzMyMSIsInVzZXJfZmxhZ3MiOjB9.Dg9p40xQW4n10dHB5KeBfF4bZIue4a2ElWHWPGnDNd7udLcuvTC3pVJeMaNw2cNQl6x9OXoASRU0jiWF8FO2Wb0sMXfrKYsQ92iGm97BLXdkHJ-mSevBfy5PqHZaz6_C25SWFCfSs8o5PWWgWvVQR2QByhbBY8Wm3pPXcgzJJgW_NaMDvvTl1_nU1-nQ-pQ6rqgAI39C6qcva2UCxnhGchZlv_x6dE7m2dTL5WztodI7CKiAbadAsfFDEF_tBZ21_tKT-up55e1TJ78N9mfE9s-3e-RQlpdsbrfbEfFkr6NJtFHCQ8KYhPdA66cSUVWYlJ9vVAxumyZsUwPR3ayz8g"

    pprint(get_data(subdomain + " ", access_token))
    pprint(get_data(subdomain + "1", access_token))
    pprint(get_data(subdomain, access_token + "1"))
    pprint(get_data(subdomain, access_token))

    #проверяем, что это это аккаунт актуального пользователя
    account = get_account(account_id)
    if not account or account.user_id != current_user.id:
        return redirect('/my.evellation')

    form = DataForm()
    if form.validate_on_submit():
        start_date = form.start_date.data
        end_date = form.end_date.data
        data_type = form.data_type.data
        print(start_date)
        return redirect(f'/my.evellation/{account_id}')
    return render_template(get_templates_name("account.html"), accounts=get_accounts(current_user.id), form=form)


@evellation_bp.route('/my.evellation/token', methods=['GET', 'POST'])
def enter_token():
    form = TokenForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()

        # получаем полбзователя
        user = get_user(current_user.id)

        # устонавливаем токен
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
