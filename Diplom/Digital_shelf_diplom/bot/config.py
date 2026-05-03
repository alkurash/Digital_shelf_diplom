# Токен, переменные окружения
# Цель: Конфигурация бота и системы
# Параметры:

# TELEGRAM_TOKEN - токен бота
# DATABASE_URL - подключение к БД
# NEURAL_MODULE_PATH - путь к модели YOLOv8
# PLANOGRAM_PATH - путь к эталонным планограммам
# TEMP_PHOTOS_DIR - директория для временных фото
# REPORTS_DIR - директория для отчётов
# CONFIDENCE_THRESHOLD - порог уверенности детекции (0.5-0.7)
# IOU_THRESHOLD - порог IoU для сопоставления с планограммой
# ALLOWED_USERS - список разрешённых пользователей
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()



# Пути к моделям нейросети
BASE_DIR = Path(__file__).parent.parent
WEIGHTS_ALL = BASE_DIR / "neural_module" / "models" / "best_2.pt"
WEIGHTS_VOID = BASE_DIR / "neural_module" / "models" / "shelf_void_detector.pt"