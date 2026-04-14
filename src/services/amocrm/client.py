import requests

from . import setup_logger  # объект логирования

# импортируем ссылки
from . import APIEndpoints

from . import events_filter

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
        return

    # обрабатываем данные
    if response.status_code == 200:
        events = response.json()
        logger.info(f'{subdomain}: Данные успешно получены')
        return events_filter(events, start_date, end_date)
    else:
        error_text = response.text if response.text else None
        logger.error(f'{subdomain}: Ошибка: {response.status_code}, {error_text}')
        return


if __name__ == "__main__":
    # тестовыем импорты для запуска из этого файла
    from src.services.amocrm.endpoints import APIEndpoints
    from src.services.amocrm.utils import events_filter

    logger = setup_logger("app_logs.log", "amo_api.log")
    from pprint import pprint
    from datetime import datetime

    start = datetime(2026, 3, 31, 21, 55)
    end = datetime(2026, 4, 16)

    pprint(get_events("rrrrt7tttttt",
                      "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6Ijg4MTEzYTg3NDgwYTk3NTExOTE4ZTJhZTI5ZjdjNGMxNzZlYTQzMGE3Y2EwM2ExY2E0YTdiMTBiN2FhYjRkZWRhZDViMjJhMGQ3NTVjYmZkIn0.eyJhdWQiOiI3YjQ5MGYxOC0yYmU1LTRhNTUtYTc0ZS0xOTYzYzk2NDFiOTgiLCJqdGkiOiI4ODExM2E4NzQ4MGE5NzUxMTkxOGUyYWUyOWY3YzRjMTc2ZWE0MzBhN2NhMDNhMWNhNGE3YjEwYjdhYWI0ZGVkYWQ1YjIyYTBkNzU1Y2JmZCIsImlhdCI6MTc3NjE4MDgyMSwibmJmIjoxNzc2MTgwODIxLCJleHAiOjE3NzYxODMyMjAsInN1YiI6IjEzNjczODcwIiwiZ3JhbnRfdHlwZSI6IiIsImFjY291bnRfaWQiOjAsImJhc2VfZG9tYWluIjpudWxsLCJ2ZXJzaW9uIjoxLCJzY29wZXMiOlsiY2hhdHMiLCJjcm0iLCJtYWlsIiwibm90aWZpY2F0aW9ucyIsInVuc29ydGVkIl0sImhhc2hfdXVpZCI6ImQxZmU3ZTU0LTZmNDktNDJmMS1iNDQzLTc3YmI5MmE5OGY0NiIsInVzZXJfZmxhZ3MiOjB9.V7-bG_dN6eZW2PL4OHH0THuA1hzmTU8Flf9k82jBabhmyuAo6UjmtY6B6BQBmzSAN1iJpqzwuRxQIwSYOGAeXrBhFd2tzeiwcmjlMwEdrWj_waoxWuxD8dUV8lA4QRstPajqKW3ZVo94qVDbkbY6W770iampRhvgnRzRl2e0K5FgyP28LdGpn1G-Xf10dHiMYIcYfnzwqi6K6qE3L9aZUUNO3rXq3pnOBb3TNEz6ZWbQFr04zW4MSP25Wq638lsgvOrdrGHlt2z8718RCnJJvgDmrC7fn7NnxMSRWtmHWE5AOMmaj5jOCZ4YixTeRP0na5DaP6RsbUHDPJBUE_pM4w",
                      start, end, None))
