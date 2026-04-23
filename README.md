# Evellation

```
Evellation ── простой способ отменять события amoCRM.
```

## Описание

В amocrm есть список событий (amocrm.ru/events/list/). Evellation позволяет **отменить** события из списка,
предоставляя работу с такими типами событий: 

| тип события                 | перевод                            |
|-----------------------------|------------------------------------|
| lead_status_changed         | Изменение этапа продажи            |
| entity_tag_added            | Теги добавлены                     |
| entity_tag_deleted	         | Теги убраны                        |
| sale_field_changed	         | Изменение поля “Бюджет”            |
| name_field_changed	         | Изменение поля “Название”          |
| entity_responsible_changed	 | Ответственный изменен              |
    
Чтобы начать работу, необходимо получить access_token.
1. https://www.amocrm.ru
2. Инструменты разработчика (<kbd>CTRL</kbd> + <kbd>SHIFT</kbd> + <kbd>I</kbd>) 
3. Application
4. Cookies
5. https://your_subdomain.amocrm.ru 
6. access_token
---

## Быстрый старт

```bash
git clone https://git@git.sourcecraft.dev/evgenii-muraviv/amo-api.git
cd amo-api
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