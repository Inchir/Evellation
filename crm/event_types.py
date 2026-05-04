from crm.models import create_session
from crm.models import Events_type

from functools import lru_cache


@lru_cache(maxsize=1)
def get_event_types():
    """Получаем все типы событий, с которыми может работать программа.
    Кэшируем результат"""
    with create_session() as db_sess:
        print("getting event type")
        print(db_sess.query(Events_type).all())
        return db_sess.query(Events_type).all()



def reload_event_types():
    """Очищает кэш.
    Использовать в случае добавление типов в БД"""
    get_event_types.cache_clear()
    return get_event_types()
