# Цель: Клавиатуры для интерфейса бота
# Методы:

# get_main_menu() - главное меню (Загрузить фото / Отчёты / Статистика)
# get_report_period_keyboard() - выбор периода отчёта
# get_store_selection_keyboard() - выбор магазина
# get_product_filter_keyboard() - фильтр по продуктам
# get_confirmation_keyboard() - кнопки подтверждения

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_kb():
    kb = [
        [KeyboardButton(text="📊 Получить отчёт")], # Текст должен совпадать с F.text в хендлере
        [KeyboardButton(text="📈 Статистика")]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)