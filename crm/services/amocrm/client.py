import requests

from crm.logger import setup_logger  # объект логирования

# импортируем ссылки
from .endpoints import APIEndpoints

# импорт дополнительных функций
from .utils import events_filter
from crm.event_types import get_event_types

logger = setup_logger("app_logs.log", "./services/amocrm/amo_api.log")


# получаем список сделок
def get_events(subdomain, access_token, start_date, end_date, event_type, created_by):
    """Получаем события (только сделки)
    фильтрует по дате (с помощью events_filter)
    и по типу события"""
    params = {
        'filter[entity]': 'lead',  # тип объекта
        'with': 'lead_name',
        'limit': 50
    }
    if event_type:
        params['filter[type]'] = event_type  # указываем тип события
    else:
        params['filter[type][]'] = [event.name for event in get_event_types()]  # если выбраны ВСЕ типы, показываем те, с которыми умеем работать
    if created_by: params['filter[created_by]'] = created_by  # указываем id автора
    # пытаемся получить данные
    try:
        response = requests.get(APIEndpoints.BASE_URL(subdomain),
                                headers=APIEndpoints.HEADERS(access_token),
                                params=params)
    except Exception as error:
        logger.error(f'{subdomain}: Ошибка: {error}')
        return None, 501  # код о внутренней ошибке (с моей стороны)

    # обрабатываем данные
    if response.status_code == 200:
        events = response.json()
        logger.info(f'{subdomain}: Данные успешно получены')
        events = events_filter(events, start_date, end_date)
        return events, 200
    else:
        error_text = response.text if response.text else None
        logger.error(f'{subdomain}: Ошибка: {response.status_code}, {error_text}')
        return None, response.status_code


def edit_leads(subdomain, access_token, params: list[dict]):
    """Получает список сделок [{'index': index, 'id': id, key: 'new value'}, ]
    И обновляет значения"""
    # пытаемся получить данные
    try:
        response = requests.patch(APIEndpoints.LEADS_URL(subdomain),
                                  headers=APIEndpoints.HEADERS(access_token),
                                  json=params)
    except Exception as error:
        logger.error(f'{subdomain}: Ошибка: {error}')
        return 501  # код о внутренней ошибке (с моей стороны)

    # обрабатываем данные
    if response.status_code == 200:
        logger.info(f'{subdomain}: Сделки успешно изменены')
        return 200
    else:
        error_text = response.text if response.text else None
        logger.error(f'edit_leads, {subdomain}: Ошибка: {response.status_code}, {error_text}')
        return response.status_code


def get_user_by_id(subdomain, access_token, user_id):
    # пытаемся получить данные
    try:
        response = requests.get(APIEndpoints.GET_USER_URL(subdomain, user_id),
                                headers=APIEndpoints.HEADERS(access_token))
    except Exception as error:
        logger.error(f'{subdomain}: Ошибка: {error}')
        return None, 501  # код о внутренней ошибке (с моей стороны)

    # обрабатываем данные
    if response.status_code == 200:
        logger.info(f'{subdomain}: Сделки успешно изменены')
        return response.json(), 200
    else:
        error_text = response.text if response.text else None
        logger.error(f'{subdomain}, {user_id}: Ошибка: {response.status_code}, {error_text}')
        return None, response.status_code



def get_lead_status(subdomain, access_token, pipeline_id, lead_status_id):
    """Получаем название этапа продажи для событий типа 'Изменение этапа продажи'"""
    # пытаемся получить данные
    try:
        response = requests.get(APIEndpoints.GET_LEAD_STATUS(subdomain, pipeline_id, lead_status_id),
                                headers=APIEndpoints.HEADERS(access_token))
    except Exception as error:
        logger.error(f'{subdomain}: Ошибка: {error}')
        return None, 501  # код о внутренней ошибке (с моей стороны)

    # обрабатываем данные
    if response.status_code == 200:
        logger.info(f'{subdomain}: Этапы продажи успешно получены')
        return response.json(), 200
    else:
        error_text = response.text if response.text else None
        logger.error(f'{subdomain}, {pipeline_id}, {lead_status_id}: Ошибка: {response.status_code}, {error_text}')
        return None, response.status_code
