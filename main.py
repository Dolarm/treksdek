import requests
import json
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Функция для запроса статуса по трек-номеру
def get_status_from_sdek_api(track_number):
    url = f'https://www.cdek.ru/api-site/track/info/?track={track_number}&locale=ru'
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверка на ошибки запроса

        if response.headers.get('Content-Type') == 'application/json':
            data = response.json()
        else:
            # Сохраняем ответ как info.json
            with open("info.json", "wb") as f:
                f.write(response.content)

            # Читаем данные из файла
            with open("info.json", "r", encoding="utf-8") as f:
                data = json.load(f)

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


# Стартовая функция для бота
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Введите трек-номер для отслеживания посылки.')

# Функция для обработки трек-номера
def handle_track_number(update: Update, context: CallbackContext) -> None:
    track_number = update.message.text
    status = get_status_from_sdek_api(track_number)
    
    if isinstance(status, dict):
        response_text = (
            f"Статус: {status['name']}\n"
            f"Код: {status['code']}\n"
            f"Дата: {status['date']}"
        )
    else:
        response_text = status
    
    update.message.reply_text(response_text)
    update.message.reply_text('Спасибо за использование бота!')

# Основная функция для запуска бота
def main() -> None:
    # Здесь вставьте токен вашего бота
    updater = Updater("7908039654:AAHbcKWcSWPp_Z82rbEoK-aDkIPD-sJcV94")

    # Получаем диспетчер для регистрации обработчиков
    dispatcher = updater.dispatcher

    # Обработчики команд и сообщений
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_track_number))

    # Запуск бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
