from datetime import datetime
from pprint import pprint


def get_value(event, value_type):
    try:
        next(iter(event['value_before'][0].values()), None) if event['value_before'] else None
    except Exception as e:
        return None


def events_filter(data, start_date, end_date):
    format_data = []
    for event in data['_embedded']['events']:
        created_data = datetime.fromtimestamp(float(event['created_at']))
        creator_id = event['created_at']
        object_name = "Сделка"
        name = event['_embedded']['entity']['name']
        event_type = event['type']
        value_before =next(iter(event['value_before'][0].keys()), None) if event['value_before'] else None
        value_after = next(iter(event['value_after'][0].keys()), None) if event['value_after'] else None
        if start_date <= datetime.fromtimestamp(float(event['created_at'])) <= end_date:
            format_data.append([created_data, creator_id, object_name, name, event_type, value_before, value_after])
    return format_data
