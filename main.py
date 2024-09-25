import asyncio
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
import logging

API_TOKEN = '7908039654:AAHbcKWcSWPp_Z82rbEoK-aDkIPD-sJcV94'  # Замените на токен вашего бота

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

async def get_tracking_info(track_number):
    url = f"https://www.cdek.ru/api-site/track/info/?track={track_number}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    
    # Проверка успешности запроса
    if response.status_code != 200:
        logger.error(f"Error: Received status code {response.status_code} for track number {track_number}")
        return None
    
    try:
        data = response.json()
    except ValueError:
        logger.error("Error: Received non-JSON response")
        logger.error("Response text: %s", response.text)
        return None
    
    return data.get("data", {}).get("status")

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.reply("Привет! Используйте команду /track <номер_отслеживания>, чтобы получить статус посылки.")

@dp.message_handler(commands=['track'])
async def track_number_handler(message: types.Message):
    try:
        track_number = message.text.split()[1]
    except IndexError:
        await message.reply("Пожалуйста, укажите номер отслеживания.")
        return
    
    status = await get_tracking_info(track_number)
    
    if status is None:
        await message.reply("Не удалось получить информацию о треке. Пожалуйста, попробуйте позже.")
    else:
        await message.reply(f"Статус трека: {status['name']}, Дата: {status['date']}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
