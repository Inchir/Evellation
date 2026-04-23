# Evellation

```
Evellation ── простой способ отменять события https://www.amocrm.ru.
```

## Описание

```
В amocrm есть список событий (amocrm.ru/events/list/). Evellation позволяет **отменить** события из списка,
предоставляя работу с такими типами сделок: 
    lead_status_changed	Изменение этапа продажи
    entity_tag_added	Теги добавлены
    entity_tag_deleted	Теги убраны
    sale_field_changed	Изменение поля “Бюджет”
    name_field_changed	Изменение поля “Название”
    entity_responsible_changed	Ответственный изменен
Чтобы начать работу, необходимо всавить access_token.
Чтобы получить: amocrm -> Инструменты разработчика -> Application -> Cookies -> https://ваш_субдомен.amocrm.ru -> access_token
```

---

## Быстрый старт

```bash
git clone <repo_url>
cd <project_name>
pip install -r requirements.txt
python main.py
```

---

## Структура проекта

```
crm/main.py - точка входа
crm/routes - основная логика
crm/services/amocrm - работа с api amocrm

```

---