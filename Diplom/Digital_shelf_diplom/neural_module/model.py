# Цель: Утилиты для работы с моделью
# Методы:

# load_yolo_model(weights_path) - загрузка обученной модели
# validate_model(model, test_dataset) - валидация на тестовом датасете
# calculate_metrics(predictions, ground_truth) - расчёт mAP, precision, recall
# export_model(model, format='onnx') - экспорт модели для продакшена
# train_model(data_yaml, epochs) - (опционально) дообучение модели

import cv2
import numpy as np
import base64
from groq import AsyncGroq # Используем асинхронный клиент для Telegram-бота

async def analyze_shelf_with_llm(
    img_bgr: np.ndarray, 
    n_products: int, 
    n_voids: int, 
    void_positions: list[str], 
    api_key: str
) -> str:
    """
    Отправляет изображение и данные детекции в LLM (Groq) для анализа.
    """
    if not api_key:
        return "❌ Ошибка: API-ключ не предоставлен."

    try:
        # Кодируем изображение в base64
        _, buf = cv2.imencode(".jpg", img_bgr, [cv2.IMWRITE_JPEG_QUALITY, 85])
        img_b64 = base64.b64encode(buf.tobytes()).decode("utf-8")

        # Формируем текст позиций
        pos_text = (
            "\n".join(f"  • {p}" for p in void_positions)
            if void_positions else "  • пустых мест не обнаружено"
        )
        
        # Промпт
        prompt = (
            f"Ты — опытный мерчандайзер. Кратко проанализируй полку магазина.\n"
            f"Данные детектора: товаров={n_products}, пустых мест={n_voids}\n"
            f"Пустые зоны: {', '.join(void_positions) if void_positions else 'не обнаружено'}\n\n"
            f"Ответь строго в таком формате (без markdown, без звёздочек, без формул):\n\n"
            f"ПУСТЫЕ МЕСТА:\n"
            f"- [название полки]: вероятно стоял [название товара]\n\n"
            f"КРИТИЧНОСТЬ: [низкая/средняя/высокая] — [одно предложение почему]\n\n"
            f"ДЕЙСТВИЕ: [одно конкретное действие для персонала]\n\n"
            f"В конце добавь короткую личную благодарность сотруднику за бдительность, "
            f"неформально и тепло, 1-2 предложения."
        )

        client = AsyncGroq(api_key=api_key)
        response = await client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {
                        "url": f"data:image/jpeg;base64,{img_b64}"
                    }},
                ],
            }],
            max_tokens=1024,
            temperature=0.3,
        )
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        return f"❌ Ошибка при запросе к LLM: {e}"