import requests

from src.logger import setup_logger

logger = setup_logger("app_logs.log", "./services/amocrm/amo_api.log")

from . import APIEndpoints


# получаем данные клиента
def get_data(subdomain, access_token):
    """получаем события (только сделки)"""
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    params = {
        'filter[entity]': 'lead',  # тип объекта
        'with': 'lead_name',
        'filter[type]': 'lead_status_changed',  # Тип события
        'limit': 50
    }

    # пытаемся получить данные
    try:
        response = requests.get(APIEndpoints.BASE_URL(subdomain), headers=headers, params=params)
    except Exception as error:
        logger.error(f'{subdomain}: Ошибка: {error}')
        return

    # обрабатываем данные
    if response.status_code == 200:
        events = response.json()
        logger.info(f'{subdomain}: Данные успешно получены')
        return events
    else:
        error_text = response.text if response.text else None
        logger.error(f'{subdomain}: Ошибка: {response.status_code}, {error_text}')
        return
