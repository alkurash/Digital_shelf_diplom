# Цель: Сопоставление детекций с планограммой
# Класс PlanogramChecker:

# __init__(planogram_data) - загрузка эталонной планограммы
# load_planogram(json_path) - чтение планограммы из JSON
# match_detections(detected_objects, planogram) - сопоставление объектов
# calculate_iou(box1, box2) - расчёт IoU между боксами
# find_violations(matched_objects) - поиск нарушений:

# Отсутствующие продукты
# Неправильное расположение
# Неправильная ориентация
# Смешение SKU


# calculate_compliance_score(violations, total_items) - % соответствия
# generate_recommendations(violations) - рекомендации по исправлению