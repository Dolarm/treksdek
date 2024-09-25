import requests
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Вставьте ваш токен и куки
TOKEN = '7908039654:AAHbcKWcSWPp_Z82rbEoK-aDkIPD-sJcV94'
COOKIES = {
    "flomni_5d713233e8bc9e000b3ebfd2": "{\"userHash\":\"82a3e68d-f455-4314-849d-79af3d757b00\"}",
    "mindboxDeviceUUID": "545e7657-f876-4820-a399-7fe8aab7ab7e",
    "directCrm-session": "%7B%22deviceGuid%22%3A%22545e7657-f876-4820-a399-7fe8aab7ab7e%22%7D",
    "_ym_uid": "1722518443262431028",
    "_ym_d": "1722518443",
    "popmechanic_sbjs_migrations": "popmechanic_1418474375998%3D1%7C%7C%7C1471519752600%3D1%7C%7C%7C1471519752605%3D1",
    "_ga": "GA1.2.350218739.1727181904",
    "_hjSessionUser_2789807": "eyJpZCI6ImQxOWYxY2UwLTVlNDEtNTJiNS04NGVhLWFkMDMyNjE4OWMzNyIsImNyZWF0ZWQiOjE3MjcxODE5MDQ3NzIsImV4aXN0aW5nIjpmYWxzZX0=",
    "_ga_LZTKRTK8Y3": "GS1.2.1727181904.1.0.1727181904.0.0.0",
    "_ga_JHC7Q4D2TV": "GS1.1.1727181903.1.0.1727181914.0.0.0",
    "_ga_2WTG9R5XMR": "GS1.1.1727181903.1.0.1727181914.49.0.0",
    "_ga_8NWQ0M7F00": "GS1.1.1727181903.1.0.1727181914.0.0.0",
    "spid": "1727181950415_c75ea0de3e8730023bc0edd0b63474bd_9x59hfpwdusuve0o",
    "advcake_track_id": "e9e586a4-c090-e62e-7578-d3dbb6e91b80",
    "advcake_session_id": "88b13de3-00f7-6da1-f298-c2cea8b06e9d",
    "sbjs_migrations": "1418474375998%3D1",
    "sbjs_first_add": "fd%3D2024-09-24%2015%3A45%3A54%7C%7C%7Cep%3Dhttps%3A%2F%2Fwww.cdek.ru%2Fru%2Ftracking%2F%7C%7C%7Crf%3Dhttps%3A%2F%2Fwww.google.com%2F",
    "sbjs_current": "typ%3Dorganic%7C%7C%7Csrc%3Dgoogle%7C%7C%7Cmdm%3Dorganic%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29",
    "sbjs_first": "typ%3Dorganic%7C%7C%7Csrc%3Dgoogle%7C%7C%7Cmdm%3Dorganic%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29",
    "cpss": "eyJ0b2tlbiI6InBoaWVZaWFzaDNpUnUzYWgifQ%3D%3D",
    "consent-to-use-of-cookies": "true",
    "advcake_track_url": "%3D20240923jXYF1btMdaMG4KK9%2FR7HB%2BQb3oCxxda9o7HFyU9BdfMoCd%2F9I6uuaOqOkgVPsjdeN5IdTAsFH0yyx4g5Il1CKwCxVEdrkSIzSP8%2BDtr06G5pqGlUhShiWpHMuj8J%2B139R5EmPj5OLE%2Bt%2F8nJXcMhwEhNAEWQU8CR%2FvcpPSGK%2BM6rT45FySJVdgZE%2B8YZQB%2BN4IDl4M8hJVhkNlCgp5KzifN%2FsLEBWB9gPXpJOOHQ9XzGQQE%2BWZFvvFZoPFob2vq%2Bepztav%2Fk2YII0rHUt3Ttg9iSApF4bMum4D7nv14wtx%2FImk7ghzq1bClkgGW6rZYD4DM4oTT3rHwRoq2hM1jNAG2ZpoEZrCForiuardcX0810buTZVnNFnFRnZs8h%2FwC%2Fx9aZZabKpf5AdhhM8rVP%2F%2FHNbf2yGLnXDYwoBL%2FqyF57%2B6PdvoIXnt5NDqOzDaB9zoMPgaPPWGBBldY5oVODjQK1eBZ%2FwV8F13K9586PvlkR%2B08EsUEmjg3fcucvaDcpruBCehjA67rIPac2JvCwrommCBCJDoR4a0tBJbi%2FbRfx6qAnd5NUXoZFL%2BzYnIYFpjbaOscdpdD7dUEIkqOdNVlonOO6lyRfpxVMBJeJIlRzmTkQ6KxeQ7HAoQeF6uTcOLGgHrjtOCgcwmGL7BpqWfaAMh8fLIcN2lsEcgdvb8ZpfncM5YSfpe4%3D",
    "sbjs_current_add": "fd%3D2024-09-25%2010%3A53%3A35%7C%7C%7Cep%3Dhttps%3A%2F%2Fwww.cdek.ru%2Fru%2Ftracking%2F%3Forder_id%3D1551855898%7C%7C%7Crf%3Dhttps%3A%2F%2Fwww.google.com%2F",
    "sbjs_udata": "vst%3D3%7C%7C%7Cuip%3D%28none%29%7C%7C%7Cuag%3DMozilla%2F5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F124.0.0.0%20Safari%2F537.36",
    "spsc": "1727272518003_4345e95b34004b60e22aeb6d484a9a4d_2dc4c47e5beb4aae25be080fa9d16c8093e7e989cef732b63b8bada59af3d7da",
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
        f'https://www.cdek.ru/api/v2/tracking/{order_id}',
        cookies=COOKIES,
        headers=headers
    )

    if response.ok:
        data = response.json()
        # Обработка данных для ответа пользователю
        status = data.get('status', 'Неизвестный статус')
        update.message.reply_text(f'Статус вашей посылки: {status}')
    else:
        update.message.reply_text('Не удалось получить данные о посылке. Проверьте номер и попробуйте снова.')

def main() -> None:
    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, track_parcel))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
