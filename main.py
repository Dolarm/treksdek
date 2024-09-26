import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Функция для запроса статуса по трек-номеру
def get_status_from_sdek_api(track_number):
    url = f'https://www.cdek.ru/api-site/track/info/?track={track_number}&locale=ru'
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Cookie': 'flomni_5d713233e8bc9e000b3ebfd2={%22userHash%22:%2282a3e68d-f455-4314-849d-79af3d757b00%22}; mindboxDeviceUUID=545e7657-f876-4820-a399-7fe8aab7ab7e; directCrm-session=%7B%22deviceGuid%22%3A%22545e7657-f876-4820-a399-7fe8aab7ab7e%22%7D; _ym_uid=1722518443262431028; _ym_d=1722518443; popmechanic_sbjs_migrations=popmechanic_1418474375998%3D1%7C%7C%7C1471519752600%3D1%7C%7C%7C1471519752605%3D1; _ga=GA1.2.350218739.1727181904; _hjSessionUser_2789807=eyJpZCI6ImQxOWYxY2UwLTVlNDEtNTJiNS04NGVhLWFkMDMyNjE4OWMzNyIsImNyZWF0ZWQiOjE3MjcxODE5MDQ3NzIsImV4aXN0aW5nIjpmYWxzZX0=; _ga_LZTKRTK8Y3=GS1.2.1727181904.1.0.1727181904.0.0.0; _ga_JHC7Q4D2TV=GS1.1.1727181903.1.0.1727181914.0.0.0; _ga_2WTG9R5XMR=GS1.1.1727181903.1.0.1727181914.49.0.0; _ga_8NWQ0M7F00=GS1.1.1727181903.1.0.1727181914.0.0.0; spid=1727181950415_c75ea0de3e8730023bc0edd0b63474bd_9x59hfpwdusuve0o; advcake_track_id=e9e586a4-c090-e62e-7578-d3dbb6e91b80; advcake_session_id=88b13de3-00f7-6da1-f298-c2cea8b06e9d; sbjs_migrations=1418474375998%3D1; sbjs_first_add=fd%3D2024-09-24%2015%3A45%3A54%7C%7C%7Cep%3Dhttps%3A%2F%2Fwww.cdek.ru%2Fru%2Ftracking%2F%7C%7C%7Crf%3Dhttps%3A%2F%2Fwww.google.com%2F; sbjs_current=typ%3Dorganic%7C%7C%7Csrc%3Dgoogle%7C%7C%7Cmdm%3Dorganic%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29; sbjs_first=typ%3Dorganic%7C%7C%7Csrc%3Dgoogle%7C%7C%7Cmdm%3Dorganic%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29; cpss=eyJ0b2tlbiI6InBoaWVZaWFzaDNpUnUzYWgifQ%3D%3D; consent-to-use-of-cookies=true; _ym_isad=2; sbjs_udata=vst%3D4%7C%7C%7Cuip%3D%28none%29%7C%7C%7Cuag%3DMozilla%2F5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F124.0.0.0%20Safari%2F537.36; cityid=435; advcake_track_url=%3D20240923NRzmY7AumtcLO1ipdca99Ai4tyz%2Fz1yuasfsC7fojJBGTtigOzFe20IQomyxrAP%2FAiXf5oZhEeEukWrk11kHd5lhUshzy%2FfY%2BXsXu3IItSyIbGr3rEaAzX%2BDxHm%2Bb%2FdwucKwDbJ3krYmp2dkWIhxfibUpLBgZH%2BBuY4K6xs3FZRzKuoKVtLeYm2QXyFKjXof0UA06utI2spHKRmzeQCkjSPnRXerHsPMP%2F6uS8YcAphNzfAzvBCrEIfsLPLvr%2F49qD9aBqqKTG1ABxX78pbyL2ki225i9c31hE8V9rdHYKHVfIW4VHuRabiv1I4NKgPnZ8tPGgBsfOMHws0cxPJTGx3VbvwJUfAkm0VrqzC3weu0l1t8oU1RthJNJClljibBavgOfW9hfnYgc9m%2B7B%2BpBGIHrX66wMIkM1JpWh5wJMAY7nty9Lt7XqmgTRzzSaWJVKu9hmEtq8O8GRb%2FIBfIQnqi6SP2V0GwMoD0TeMwuHLhGLcN%2BNLXtrKA0WyeecaF2mx1J%2BymvRyiK%2FLpgmVCowtRnoJzza1xc4FcH%2BtNkXYi22cjqpsuDea5Brq%2Fm3P1bQHoAZ%2BOGd5yhVytmmpUSaiC0qP8ktF9S%2BBqIzRRxSBoqxA6YXbNIPKTxOuPChGNoQJIaYTbthGvsT3ry3vlnrgcW3YWTYaLXJOXcsn9KBUQ%2BE74MXJn4DU%3D'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Проверка на ошибки запроса
        data = response.json()

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

# Стартовая функция для бота, которая запрашивает трек-номер
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Введите трек-номер для отслеживания посылки.')

# Функция для обработки трек-номера и отправки статуса
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
    update.message.reply_text("Введите другой трек-номер для продолжения.")

# Основная логика запуска бота
def main():
    updater = Updater("7908039654:AAHbcKWcSWPp_Z82rbEoK-aDkIPD-sJcV94", use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_track_number))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
