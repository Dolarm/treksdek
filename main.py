import requests
import json

def get_status_from_sdek_api(track_number):
    url = f'https://www.cdek.ru/api-site/track/info/?track={track_number}&locale=ru'
    
    try:
        response = requests.get(url)

        # Проверяем на успешность запроса
        response.raise_for_status()

        # Если ответ в виде JSON
        if response.headers.get('Content-Type') == 'application/json':
            data = response.json()
        else:
            # Если ответ пришёл в виде файла, сохраняем его и читаем как JSON
            with open("info.json", "wb") as f:
                f.write(response.content)

            # Открываем и читаем JSON из файла
            with open("info.json", "r", encoding="utf-8") as f:
                data = json.load(f)

        # Извлекаем статус посылки
        status = data.get('status', {})
        if status:
            return {
                'code': status.get('code', 'Неизвестно'),
                'name': status.get('name', 'Неизвестно'),
                'date': status.get('date', 'Неизвестно')
            }
        else:
            return "Статус не найден."

    except requests.exceptions.RequestException as e:
        return f"Ошибка запроса: {str(e)}"


# Пример использования:
track_number = "1551855898"
status = get_status_from_sdek_api(track_number)
print(status)
