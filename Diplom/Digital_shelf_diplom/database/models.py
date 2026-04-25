# Цель: ORM-модели базы данных
# Модели:
# Detection (результаты детекции):

# id - первичный ключ
# photo_path - путь к оригинальному фото
# annotated_photo_path - путь к аннотированному фото
# detection_results - JSON с координатами объектов
# user_id - ID пользователя Telegram
# store_id - FK на магазин
# timestamp - время загрузки
# processing_time - время обработки

# Report (отчёты о соответствии):

# id - первичный ключ
# detection_id - FK на Detection
# compliance_percentage - процент соответствия планограмме
# violations - JSON с нарушениями
# recommendations - рекомендации
# created_at - время создания

# Product (продукты компании):

# id - первичный ключ
# name - название продукта
# category - категория
# sku - артикул
# expected_position - ожидаемая позиция на полке

# Store (магазины):

# id - первичный ключ
# name - название магазина
# address - адрес
# chain - торговая сеть