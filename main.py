import logging
import requests
import json
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Создание сессии для управления заголовками
session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
})

# Функция для получения статуса по трек-номеру через неофициальный API СДЭК
def get_status_from_sdek_api(track_number):
    url = f'https://www.cdek.ru/api-site/track/info/?track={track_number}&locale=ru'
    
    try:
        response = session.get(url)
        response.raise_for_status()  # Проверка на ошибки запроса

        if response.headers.get('Content-Type') == 'application/json':
            # Пробуем сразу разобрать JSON
            data = response.json()
        else:
            # Сохраняем ответ как info.json
            with open("info.json", "wb") as f:
                f.write(response.content)

            # Читаем данные из файла
            with open("info.json", "r", encoding="utf-8") as f:
                file_content = f.read()

            if not file_content.strip():
                return "Ошибка: файл пуст или содержит некорректные данные."

            try:
                data = json.loads(file_content)
            except json.JSONDecodeError:
                return "Ошибка: не удалось разобрать JSON из файла."

        # Проверяем статус
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

# Функция, вызываемая при команде /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Введите трек-номер, чтобы узнать статус отправления.')

# Функция для обработки трек-номера
def handle_track_number(update: Update, context: CallbackContext) -> None:
    track_number = update.message.text.strip()
    update.message.reply_text(f'Получаю статус для трек-номера: {track_number}...')
    
    # Получение статуса через API
    status = get_status_from_sdek_api(track_number)

    if isinstance(status, dict):
        # Форматируем ответ, если статус получен
        response_message = f"Статус: {status['name']}\nКод: {status['code']}\nДата: {status['date']}"
    else:
        # Если возникла ошибка
        response_message = status

    update.message.reply_text(response_message)

# Основная функция для запуска бота
def main():
    # Вставьте сюда свой токен
    updater = Updater("7908039654:AAHbcKWcSWPp_Z82rbEoK-aDkIPD-sJcV94", use_context=True)
    
    dispatcher = updater.dispatcher

    # Команда /start
    dispatcher.add_handler(CommandHandler("start", start))

    # Обработка текстовых сообщений (трек-номеров)
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_track_number))

    # Запуск бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
