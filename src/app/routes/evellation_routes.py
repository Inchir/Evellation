from flask import Blueprint
from flask import render_template, redirect
from flask_login import current_user

# формы
from . import AccountForm, TokenForm, EventsForm

# сессия
from . import db_session

# модель
from . import Account

# импортируем вспомогательные функции
from . import get_templates_name, get_user, get_account, get_accounts, create_account, set_errors

# api
from . import get_events

import logging

# Create a blueprint instance
evellation_bp = Blueprint('evellation', __name__)


@evellation_bp.route('/my.evellation')
def my_evellation():
    return render_template(get_templates_name("base.html"), accounts=get_accounts(current_user.id))


@evellation_bp.route('/my.evellation/<account_id>', methods=['GET', 'POST'])
def my_evellation_account(account_id):
    # проверяем, что это это аккаунт актуального пользователя
    account = get_account(account_id)
    if not account or account.user_id != current_user.id:
        return redirect('/my.evellation')

    form = EventsForm()
    form.set_events_form_choices(db_session)
    if form.validate_on_submit():
        try:
            account = get_account(account_id)
            start_date = form.start_date.data
            end_date = form.end_date.data
            event_type = form.event_type.data
            events, status_code = get_events(account.subdomain, current_user.token,
                                             start_date, end_date, event_type)
            if not events: events = []
            errors = set_errors(status_code)
            return render_template(get_templates_name("account.html"), accounts=get_accounts(current_user.id),
                                   form=form,
                                   events=events, errors=errors)
        except Exception as e:
            logging.error(f"ошибка в my_evellation_account: {e}")
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
def my_evellation_create_account():
    form = AccountForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(Account).filter(Account.name == form.name.data,
                                         Account.user_id == current_user.id).first():
            return render_template(get_templates_name("create_account.html"), form=form,
                                   message="Аккаунт с таким названием уже есть")
        # создаем аккаунт
        account = create_account(form)

        # сохраняем
        db_sess.add(account)
        db_sess.commit()

        return redirect('/my.evellation')

    return render_template(get_templates_name("create_account.html"), form=form)
