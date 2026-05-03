# Цель: Точка входа в бота
# Методы:

# async def main() - инициализация бота и диспетчера
# setup_handlers(dp) - регистрация всех обработчиков
# setup_database() - инициализация подключения к БД
# on_startup() - действия при запуске
# on_shutdown() - корректное завершение работы
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from bot.config import BOT_TOKEN
from bot.handlers import photo_handler, report_handler
from bot.keyboards import get_main_kb
# Импортируем функцию инициализации
from database.db import init_db 

logging.basicConfig(level=logging.INFO)

async def main():
    # 1. Инициализируем базу данных перед запуском бота
    init_db() 
    
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(photo_handler.router)
    dp.include_router(report_handler.router)

    @dp.message(Command("start"))
    async def cmd_start(message: types.Message):
        await message.answer(
            f"Привет, {message.from_user.full_name}! Я бот 'Retail Vision'.\n"
            "Пришли мне фото полки для анализа.",
            reply_markup=get_main_kb()
        )

    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())