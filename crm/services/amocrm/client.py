import requests

from crm.logger import setup_logger  # объект логирования

# импортируем ссылки
from .endpoints import APIEndpoints

# импорт дополнительных функций
from .utils import events_filter

logger = setup_logger("app_logs.log", "./services/amocrm/amo_api.log")


# получаем данные клиента
def get_events(subdomain, access_token, start_date, end_date, event_type):
    """получаем события (только сделки)
    фильтрует по дате (с помощью events_filter)
    и по типу события"""
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    params = {
        'filter[entity]': 'lead',  # тип объекта
        'with': 'lead_name',
        'limit': 50
    }
    if event_type: params['filter[type]'] = event_type  # Тип события

    # пытаемся получить данные
    try:
        response = requests.get(APIEndpoints.BASE_URL(subdomain), headers=headers, params=params)
    except Exception as error:
        logger.error(f'{subdomain}: Ошибка: {error}')
        return None, 501  # код о внутренней ошибке (с моей стороны)

    # обрабатываем данные
    if response.status_code == 200:
        events = response.json()
        logger.info(f'{subdomain}: Данные успешно получены')
        return events_filter(events, start_date, end_date), 200
    else:
        error_text = response.text if response.text else None
        logger.error(f'{subdomain}: Ошибка: {response.status_code}, {error_text}')
        return None, response.status_code
