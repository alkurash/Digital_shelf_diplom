# Цель: CRUD-операции с базой данных
# Классы и методы:
# DetectionCRUD:

# create_detection(photo_path, results, user_id) - сохранение результата детекции
# get_detection_by_id(detection_id) - получение детекции по ID
# get_detections_by_date(start_date, end_date) - выборка за период
# get_detections_by_store(store_id) - детекции по магазину
# update_detection_status(detection_id, status) - обновление статуса

# ReportCRUD:

# create_report(detection_id, compliance_score, violations) - создание отчёта
# get_report_by_id(report_id) - получение отчёта
# get_reports_summary(start_date, end_date) - сводка по отчётам
# calculate_average_compliance(period) - средний процент соответствия

# ProductCRUD:

# get_all_products() - список всех продуктов компании
# get_product_by_name(name) - поиск продукта по названию