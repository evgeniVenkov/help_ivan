import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
from dotenv import load_dotenv
from GPTClient import GPTClient
from datetime import datetime



gpt_client = GPTClient()
# Загружаем токен из .env
load_dotenv()
TOKEN = os.getenv("TOKEN")

# Логирование (чтобы видеть ошибки и события)
logging.basicConfig(level=logging.INFO)

# Создаём бота и диспетчер
bot = Bot(token=TOKEN)
dp = Dispatcher()



# Команда /start
@dp.message(Command("start"))
async def start_handler(message: Message):
    user_name = message.from_user.first_name or "Безымянный злодея!"
    await message.answer(f"👋 Привет! Я бот-лекарь для {message.from_user.first_name} напиши мне что у тебя случилось?")
# Обработчик команды /start

# Команда /help
@dp.message(Command("help"))
async def help_handler(message: Message):
    await message.answer("просто напиши мне свой недуг")


@dp.message()
async def echo_message(message: Message):
    user_name = message.from_user.username or "Без ника"
    user_text = message.text

    mess_text = f"📩 Новое сообщение от {message.from_user.username} | {message.text} "

    print(mess_text)

    response = gpt_client.chat(message.text)
    with open(".logi", "a", encoding="utf-8") as log_file:
        log_file.write(f"Пользователь: {user_name}\n")
        log_file.write(f"Сообщение: {user_text}\n")
        log_file.write(f"Ответ: {response}\n")
        log_file.write("------------------------\n")

    await message.answer(response)


# Запуск бота

# Обработчик всех текстовых сообщений

# Запуск бота
async def main():
    print("✅ Бот запущен и готов к работе!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
