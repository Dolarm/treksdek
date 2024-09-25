import requests
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Вставьте ваш токен и куки
TOKEN = '7908039654:AAHbcKWcSWPp_Z82rbEoK-aDkIPD-sJcV94'
COOKIES = {
    "flomni_5d713233e8bc9e000b3ebfd2": "{\"userHash\":\"82a3e68d-f455-4314-849d-79af3d757b00\"}",
    "mindboxDeviceUUID": "545e7657-f876-4820-a399-7fe8aab7ab7e",
    "directCrm-session": "%7B%22deviceGuid%22%3A%22545e7657-f876-4820-a399-7fe8aab7ab7e%22%7D",
    # добавьте остальные куки здесь в аналогичном формате
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
}

def start(update: Update, _: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_html(
        rf"Привет, {user.mention_html()}! Я бот для отслеживания посылок.",
        reply_markup=ForceReply(selective=True),
    )

def track_parcel(update: Update, _: CallbackContext) -> None:
    order_id = update.message.text
    response = requests.get(
        f'https://www.cdek.ru/api/v2/orders/{order_id}',
        cookies=COOKIES,
        headers=headers
    )

    if response.status_code == 200:
        data = response.json()
        # Обработка данных и отправка ответа пользователю
        update.message.reply_text(f"Данные для заказа {order_id}: {data}")
    else:
        update.message.reply_text("Не удалось получить данные о посылке. Попробуйте позже.")

def main() -> None:
    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, track_parcel))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
