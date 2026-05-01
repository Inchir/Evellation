from flask_login import current_user
from datetime import datetime
from typing import Dict
import redis
import json

REDIS_LIFETIME = 3600

r = redis.Redis(
    host='redis-10536.c300.eu-central-1-1.ec2.cloud.redislabs.com',
    port=10536,
    decode_responses=True,
    socket_timeout=3,
    socket_connect_timeout=3,
    username="default",
    password="E3WHmd4iU69RQO0okSIBxq9UcUI702Ku",
)


def redis_save_events(user_id, events):
    key = f"events:{user_id}"

    data = {
        event['index']: event
        for event in events
    }

    r.setex(key, REDIS_LIFETIME, json.dumps(data))


def redis_get_event(user_id, event_index):
    key = f"events:{user_id}"

    raw = r.get(key)
    if not raw:
        return None

    data = json.loads(raw)  # type: ignore
    return data.get(event_index)


def events_filter(data, start_date, end_date):
    current_user_id = current_user.get_id()
    save_data = []
    format_data = []
    for index, event in enumerate(data['_embedded']['events'], start=0):
        event_id = event['entity_id']

        created_data = datetime.fromtimestamp(float(event['created_at']))
        creator_id = event.get('created_by', "Данных нет")
        object_name = "Сделка"
        name = event['_embedded']['entity'].get('name', "Без имени")
        event_type = event.get('type', "Данных нет")

        value_before, value_after = "", ""
        if event.get('value_before', ''):
            value_before = get_value(event['value_before'][0])

        if event.get('value_after', ''):
            value_after = get_value(event['value_after'][0])

        # сохраняем данные
        if event['type'] == 'sale_field_changed':
            # если value_before пусто, то была 0
            save_data.append({'index': index, 'id': event_id, 'price': value_before if value_before else 0})
        elif event['type'] == 'lead_status_changed':
            save_data.append({'index': index, 'id': event_id, 'status_id': value_before})
        elif event['type'] == 'name_field_changed':
            save_data.append({'index': index, 'id': event_id, 'name': value_before})
        elif event['type'] == 'entity_responsible_changed':
            save_data.append({'index': index, 'id': event_id, 'responsible_user_id': value_before})
        elif event['type'] == 'entity_tag_added':
            save_data.append({'index': index, 'id': event_id, 'tags_to_delete': [{'name': value_after}, ]})
        elif event['type'] == 'entity_tag_deleted':
            save_data.append({'index': index, 'id': event_id, 'tags_to_add': [{'name': value_before}, ]})

        if start_date <= datetime.fromtimestamp(float(event['created_at'])) <= end_date:
            format_data.append({"index": index,
                                "utils": {"id": event_id},
                                "data": {"created_data": created_data, "created_by": creator_id,
                                         "object_name": object_name, "name": name, "event_type": event_type,
                                         "value_before": value_before,
                                         "value_after": value_after}})
    # print("start save: ", save_data)
    redis_save_events(current_user_id, save_data)
    print("end_save")
    return format_data


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
