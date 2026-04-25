# # Отправка отчётов пользователю
# Цель: Генерация и отправка отчётов
# Методы:

# handle_request_report(message: Message) - обработка запроса отчёта
# generate_report_command(user_id, period) - команда на генерацию отчёта
# format_report_message(report_data) - форматирование отчёта для Telegram
# send_report_pdf(user_id, report_path) - отправка PDF-отчёта
# handle_report_filters(callback: CallbackQuery) - фильтры отчётов (дата, магазин, продукт)
# show_statistics(user_id) - показ общей статистики