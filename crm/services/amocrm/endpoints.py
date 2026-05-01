# тут все пути
class APIEndpoints:
    BASE_URL = lambda subdomain: f'https://{subdomain}.amocrm.ru/api/v4/events'
    LEADS_URL = lambda subdomain: f'https://{subdomain}.amocrm.ru/api/v4/leads'

    HEADERS = lambda access_token: {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
