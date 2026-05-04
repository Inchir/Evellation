from flask import Blueprint
from flask import render_template, redirect, request, jsonify
from flask_login import current_user

import logging

# формы
from crm.forms import AccountForm, TokenForm, EventsForm

# сессия
from crm.models import create_session

# модели
from crm.models import Account

# импортируем вспомогательные функции
from .utils import get_templates_name, get_user, get_account, get_accounts, create_account, set_errors

# api
from crm.services.amocrm import get_events, edit_leads, get_user_by_id

# redis
from crm.services.amocrm import redis_get_event

# модели
from crm.models import Events_type

# Create a blueprint instance
evellation_bp = Blueprint('evellation', __name__)


@evellation_bp.route('/my.evellation')
def my_evellation():
    return render_template(get_templates_name("base.html"), accounts=get_accounts(current_user.id))


@evellation_bp.route("/edit_events/<account_id>", methods=["POST"])
def edit_events(account_id):
    # отмена всех сделок

    print("Массовое действие!!!")

    data = request.get_json()
    events_index = data.get("events")
    account = get_account(account_id)

    data = []
    for index in events_index:
        b = redis_get_event(current_user.get_id(), str(index))
        del b['index']
        data.append(b)

    print(edit_leads(account.subdomain, current_user.token, data))
    return jsonify({"status": "ok"})


@evellation_bp.route("/edit_event/<account_id>", methods=["POST"])
def edit_event(account_id):
    data = request.get_json()
    event_index = data.get("eventIndex")
    data = redis_get_event(current_user.get_id(), str(event_index))
    del data['index']
    account = get_account(account_id)
    print(edit_leads(account.subdomain, current_user.token, [data]))

    return jsonify({"status": "ok"})


@evellation_bp.route('/my.evellation/<account_id>', methods=['GET', 'POST'])
def my_evellation_account(account_id):
    # проверяем, что это аккаунт актуального пользователя
    account = get_account(account_id)
    if not account or account.user_id != current_user.id:
        return redirect('/my.evellation')

    form = EventsForm()
    if form.validate_on_submit():
        account = get_account(account_id)
        start_date = form.start_date.data
        end_date = form.end_date.data
        event_type = form.event_type.data
        created_by = form.created_by.data

        # получаем события из amocrm api
        events, status_code = get_events(account.subdomain, current_user.token,
                                         start_date, end_date, event_type, created_by)
        if not events: events = []
        users = {0: "Робот"}  # храним id пользователя - имя
        with create_session() as db_sess:
            # английское название сделки - перевод
            translating_events = {event.name: event.translation for event in db_sess.query(Events_type).all()}
        events_index = []

        for event in events:
            events_index.append(event["index"])
            created_by = event['data']['created_by']  # id автора
            if created_by in users:
                user_name = users[created_by]
            else:
                user, status_code = get_user_by_id(account.subdomain, current_user.token, created_by)
                if status_code == 200:
                    user_name = user['name']
                else:
                    user_name = 'Нет данных'
                users[created_by] = user_name  # запоминаем пользователей, чтобы каждый раз не обращаться к api
            if event['data']['event_type'] == "entity_responsible_changed":
                value_before = event['data']['value_before']
                if value_before in users:
                    value_before = users[value_before]
                else:
                    user, status_code = get_user_by_id(account.subdomain, current_user.token, value_before)
                    if status_code == 200:
                        value_before = user['name']
                    else:
                        value_before = 'Нет данных'
                    users[event['data']['value_before']] = value_before  # запоминаем пользователей

                value_after = event['data']['value_after']
                if value_after in users:
                    value_after = users[value_after]
                else:
                    user, status_code = get_user_by_id(account.subdomain, current_user.token, value_after)
                    if status_code == 200:
                        value_after = user['name']
                    else:
                        value_after = 'Нет данных'
                    users[event['data']['value_after']] = value_after  # запоминаем пользователей

                event['data']['value_before'] = value_before
                event['data']['value_after'] = value_after
            event['data']['created_by'] = user_name
            event['utils']['subdomain'] = account.subdomain  # передаем субдомен для формирования ссылок
            event['data']['event_type'] = translating_events.get(event['data']['event_type'], event['data'][
                'event_type'])  # переводим название события, если перевода нет, оставляем как есть
        errors = set_errors(status_code)
        return render_template(get_templates_name("account.html"), accounts=get_accounts(current_user.id),
                               account_id=account_id,
                               form=form,
                               events=events, events_index=events_index, errors=errors)
    # try:
    #
    # except Exception as e:
    #     logging.error(f"ошибка в my_evellation_account: {e}")
    #     return redirect(f'/my.evellation/{account_id}')
    return render_template(get_templates_name("account.html"), accounts=get_accounts(current_user.id), form=form)


@evellation_bp.route('/my.evellation/token', methods=['GET', 'POST'])
def enter_token():
    form = TokenForm()
    if form.validate_on_submit():
        with create_session() as db_sess:
            # получаем полбзователя
            user = get_user(current_user.id)

            # устонавливаем токен
            user.token = form.token.data

            db_sess.merge(user)
            db_sess.commit()

            return redirect('/my.evellation')

    return render_template(get_templates_name("enter_token.html"), form=form)


@evellation_bp.route('/my.evellation/create.account', methods=['GET', 'POST'])
def my_evellation_create_account():
    form = AccountForm()
    if form.validate_on_submit():
        with create_session() as db_sess:
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
