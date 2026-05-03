# # Отправка отчётов пользователю
# Цель: Генерация и отправка отчётов
# Методы:

# handle_request_report(message: Message) - обработка запроса отчёта
# generate_report_command(user_id, period) - команда на генерацию отчёта
# format_report_message(report_data) - форматирование отчёта для Telegram
# send_report_pdf(user_id, report_path) - отправка PDF-отчёта
# handle_report_filters(callback: CallbackQuery) - фильтры отчётов (дата, магазин, продукт)
# show_statistics(user_id) - показ общей статистики
from aiogram import Router, types, F
from datetime import datetime, timedelta

from database import get_session, ReportCRUD

router = Router()


# 📊 Запрос отчёта
@router.message(F.text == "📊 Получить отчёт")
async def handle_request_report(message: types.Message):
    user_id = message.from_user.id
    report_text = generate_report_command(user_id, period="day")
    await message.answer(report_text)


def generate_report_command(user_id, period="day"):
    db = get_session()

    now = datetime.utcnow()

    if period == "day":
        start_date = now - timedelta(days=1)
    elif period == "week":
        start_date = now - timedelta(days=7)
    else:
        start_date = now - timedelta(days=30)

    reports = ReportCRUD.get_reports_summary(db, start_date, now)
    avg = ReportCRUD.calculate_average_compliance(db, start_date, now)

    return format_report_message(reports, avg)


def format_report_message(reports, avg):
    if not reports:
        return "❌ Нет данных за выбранный период"

    text = "📊 Отчёт по выкладке:\n\n"

    for r in reports:
        text += f"ID: {r['id']} | {r['compliance']:.1f}% | {r['date']}\n"

    text += f"\n📈 Среднее соответствие: {avg:.1f}%"

    return text


# 📈 Общая статистика
@router.message(F.text == "📈 Статистика")
async def show_statistics(message: types.Message):
    db = get_session()

    now = datetime.utcnow()
    start = now - timedelta(days=30)

    avg = ReportCRUD.calculate_average_compliance(db, start, now)

    await message.answer(
        f"📊 Статистика за 30 дней:\n"
        f"Среднее соответствие: {avg:.2f}%"
    )