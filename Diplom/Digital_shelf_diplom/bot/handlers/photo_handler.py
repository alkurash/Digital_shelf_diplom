# Обработка входящих фотографий от мерчендайзера
# Цель: Обработка загрузки фотографий от пользователей
# Методы:

# handle_photo(message: Message) - основной обработчик получения фото
# validate_photo(photo) - проверка формата и качества изображения
# save_temp_photo(photo, user_id) - сохранение фото во временное хранилище
# send_to_neural_module(photo_path) - отправка фото в нейросетевой модуль
# handle_processing_result(result) - обработка результата от нейросети
# send_annotated_image(user_id, image_path) - отправка аннотированного изображения пользователю
import io
import time
import cv2
import numpy as np
from aiogram import Router, F, types
from aiogram.types import BufferedInputFile

from neural_module.detector import RetailDetector
from neural_module.postprocessing import draw_all_detections
from neural_module.model import analyze_shelf_with_llm
from bot.config import WEIGHTS_ALL, WEIGHTS_VOID, GROQ_API_KEY

# 🔥 БД
from database import get_session, DetectionCRUD, ReportCRUD, ProductCRUD

# (если реализуешь позже)
# from neural_module.planogram_checker import check_planogram

router = Router()

detector = RetailDetector(str(WEIGHTS_ALL), str(WEIGHTS_VOID))


from contextlib import closing # Для безопасного закрытия сессии

@router.message(F.photo)
async def handle_photo(message: types.Message):
    await message.answer("🔍 Анализирую полку, подождите...")
    start_time = time.time()

    # --- 1. Загрузка фото ---
    photo_buffer = io.BytesIO()
    await message.bot.download(message.photo[-1], destination=photo_buffer)

    file_bytes = np.frombuffer(photo_buffer.getvalue(), dtype=np.uint8)
    img_bgr = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    # --- 2. Детекция ---
    results = detector.detect(img_bgr)

    # --- 3. Отрисовка ---
    processed_img = draw_all_detections(
        img_bgr,
        results["products"]["boxes"],
        results["products"]["labels"],
        results["voids"]["boxes"],
        results["voids"]["confs"]
    )

    # --- 4. LLM-анализ ---
    ai_analysis = await analyze_shelf_with_llm(
        img_bgr,
        results["products"]["count"],
        results["voids"]["count"],
        results["voids"]["positions"],
        GROQ_API_KEY
    )

    # --- 5. (опционально) Проверка планограммы ---
    # planogram_result = check_planogram(results)

    # --- 6. Сохранение в БД ---
    db = get_session()

    processing_time = time.time() - start_time

    with closing(get_session()) as db: # Сессия закроется автоматически
        processing_time = time.time() - start_time
        
        detection = DetectionCRUD.create_detection(
            db=db,
            photo_path="in_memory.jpg",
            results=results,
            user_id=message.from_user.id,
            processing_time=processing_time
        )

        compliance = 100.0
        violations = []
        if results["voids"]["count"] > 0:
            compliance -= min(results["voids"]["count"] * 10, 100)
            violations.append("Обнаружены пустоты на полке")

        ReportCRUD.create_report(
            db=db,
            detection_id=detection.id,
            compliance_score=compliance,
            violations=violations,
            recommendations="Устранить пустоты и восстановить выкладку"
        )

    # --- 8. Отправка изображения ---
    _, encoded_img = cv2.imencode(".jpg", processed_img)
    output_photo = BufferedInputFile(encoded_img.tobytes(), filename="result.jpg")

    await message.answer_photo(
        photo=output_photo,
        caption=(
            f"✅ Анализ завершен!\n\n"
            f"{ai_analysis}\n\n"
            f"📊 Соответствие: {compliance:.1f}%"
        )
    )