import re
import json
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Функция для удаления комментариев из JSON
def remove_comments_from_json(file_content):
    """Функция для удаления комментариев из JSON-строки."""
    cleaned_content = re.sub(r'//.*', '', file_content)  # Удаляем строки, которые начинаются с // (комментарии)
    return cleaned_content

# Функция для получения статуса из API СДЭК
def get_status_from_sdek_api(track_number):
    url = f'https://www.cdek.ru/api-site/track/info/?track={track_number}&locale=ru'
    
    try:
        # Отправляем запрос к API СДЭК
        response = requests.get(url)
        
        # Проверяем, что запрос был успешным
        if response.status_code != 200:
            return f"Ошибка запроса: {response.status_code}"

        # Получаем сырой JSON
        raw_content = response.text
        
        # Очищаем JSON от комментариев
        clean_json = remove_comments_from_json(raw_content)
        
        # Логирование для проверки полученного JSON
        print(f"Чистый JSON:\n{clean_json}")

        # Разбираем JSON
        data = json.loads(clean_json)
        
        # Логирование результата разбора JSON
        print(f"Разобранный JSON:\n{data}")

        # Возвращаем статус
        return data.get("data", {}).get("status", {}).get("name", "Статус не найден")
    
    except json.JSONDecodeError as e:
        return f"Ошибка разбора JSON: {str(e)}"
    except Exception as e:
        return f"Ошибка запроса: {str(e)}"

# Функция для обработки команды /start
def start(update: Update, context: CallbackContext):
    update.message.reply_text('Введите номер отслеживания СДЭК для проверки статуса.')

# Функция для обработки введённого текста (номер отслеживания)
def handle_track_number(update: Update, context: CallbackContext):
    # Получаем текст сообщения (это и будет трек-номер)
    track_number = update.message.text.strip()

    # Логируем трек-номер для отладки
    print(f"Трек-номер: {track_number}")

    # Проверяем статус заказа через API СДЭК
    status = get_status_from_sdek_api(track_number)
    
    # Логируем полученный статус для отладки
    print(f"Статус заказа: {status}")

    # Отправляем статус пользователю
    update.message.reply_text(f"Статус заказа: {status}")

# Главная функция для запуска бота
def main():
    # Создаём апдейтера и передаём в него токен вашего бота
    updater = Updater("7908039654:AAHbcKWcSWPp_Z82rbEoK-aDkIPD-sJcV94", use_context=True)
    
    # Получаем диспетчер для регистрации обработчиков
    dp = updater.dispatcher
    
    # Регистрация обработчика команды /start
    dp.add_handler(CommandHandler("start", start))
    
    # Обработчик всех текстовых сообщений (для трек-номеров)
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_track_number))

    # Запускаем бота
    updater.start_polling()

    # Ожидаем прерывания
    updater.idle()

if __name__ == '__main__':
    main()
