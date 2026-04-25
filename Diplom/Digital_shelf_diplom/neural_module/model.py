# Цель: Утилиты для работы с моделью
# Методы:

# load_yolo_model(weights_path) - загрузка обученной модели
# validate_model(model, test_dataset) - валидация на тестовом датасете
# calculate_metrics(predictions, ground_truth) - расчёт mAP, precision, recall
# export_model(model, format='onnx') - экспорт модели для продакшена
# train_model(data_yaml, epochs) - (опционально) дообучение модели