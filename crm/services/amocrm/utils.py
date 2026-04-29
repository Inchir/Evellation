from datetime import datetime
from pprint import pprint
from typing import Dict


def get_value(data: Dict):
    """Принимает словарь бесконечной вложенности,
    возвращает первое возможное значение или None
    {'key': {'key1': {'key3': 'value1'}, 'key2': 'value2'}} -> value1"""

    key = next(iter(data.keys()), None)
    if not key:
        return None
    data = data[key]
    if type(data) == dict:
        return get_value(data)
    else:
        return data


def events_filter(data, start_date, end_date):
    format_data = []
    for event in data['_embedded']['events']:
        created_data = datetime.fromtimestamp(float(event['created_at']))
        creator_id = event.get('created_at', "Данных нет")
        object_name = "Сделка"
        name = event['_embedded']['entity'].get('name', "Без имени")
        event_type = event.get('type', "Данных нет")
        value_before, value_after = '', ''
        if event.get('value_before', ''):
            value_before = get_value(event['value_before'][0])
        if event.get('value_after', ''):
            value_after = get_value(event['value_after'][0])
        if start_date <= datetime.fromtimestamp(float(event['created_at'])) <= end_date:
            format_data.append([created_data, creator_id, object_name, name, event_type, value_before, value_after])
    return format_data
