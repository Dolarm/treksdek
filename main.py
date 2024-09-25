import requests
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor

API_TOKEN = '7908039654:AAHbcKWcSWPp_Z82rbEoK-aDkIPD-sJcV94'
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Функция для получения информации о треке
def get_tracking_info(track_number):
    url = f'https://www.cdek.ru/api-site/track/info/?track={track_number}'
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            return data['data']['status']
        else:
            return {'error': 'Ошибка при получении данных'}
    else:
        return {'error': f'HTTP ошибка: {response.status_code}'}

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer("Введите номер трека:")

# Обработчик текстовых сообщений
@dp.message_handler()
async def track_number_handler(message: types.Message):
    track_number = message.text
    status = get_tracking_info(track_number)
    
    if 'error' in status:
        await message.answer(status['error'])
    else:
        await message.answer(f"Статус трека: {status['name']} (Код: {status['code']})")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
