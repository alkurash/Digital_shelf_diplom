# Цель: Класс для работы с YOLOv8
# Класс YOLODetector:

# __init__(model_path, conf_threshold) - инициализация модели
# load_model() - загрузка весов YOLOv8
# detect(image_path) - детекция объектов на изображении
# preprocess_image(image) - предобработка (resize, normalization)
# postprocess_results(raw_results) - обработка результатов (NMS, фильтрация)
# extract_bboxes(results) - извлечение bounding boxes
# get_class_names() - получение списка классов продуктов
# calculate_confidence_scores(detections) - расчёт уверенности