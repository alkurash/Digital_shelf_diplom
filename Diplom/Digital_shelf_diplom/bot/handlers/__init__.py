# # Регистрация всех обработчиков
# - Функция register_handlers(dp: Dispatcher) для регистрации всех хендлеров
from aiogram import Dispatcher

from .photo_handler import router as photo_router
from .report_handler import router as report_router


def register_handlers(dp: Dispatcher):
    dp.include_router(photo_router)
    dp.include_router(report_router)
