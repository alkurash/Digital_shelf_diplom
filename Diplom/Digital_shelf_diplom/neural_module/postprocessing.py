# Цель: Генерация аннотированных изображений
# Методы:

# draw_bboxes(image, detections, color_scheme) - отрисовка боксов
# add_labels(image, detections, font_size) - добавление меток классов
# highlight_violations(image, violations) - выделение нарушений красным
# add_compliance_badge(image, compliance_score) - бейдж с % соответствия
# create_side_by_side_view(original, annotated, planogram) - сравнение
# add_legend(image, classes) - легенда по цветам
# save_annotated_image(image, output_path) - сохранение результата

import cv2
import numpy as np
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# Цвета
COLOR_VOID = (0, 255, 0)
COLOR_PRODUCT = (255, 100, 0)
LABEL_VOID_RU = "Пустое место"

def _find_font(size: int = 18):
    """Поиск системного шрифта с кириллицей"""
    for p in [
        r"C:\Windows\Fonts\arial.ttf",
        r"C:\Windows\Fonts\Arial.ttf",
        r"C:\Windows\Fonts\segoeui.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    ]:
        if Path(p).exists():
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()

FONT_LARGE = _find_font(20)
FONT_SMALL = _find_font(16)

def draw_all_detections(
    img_bgr: np.ndarray,
    product_boxes: list,
    product_labels: list,
    void_boxes: list,
    void_confs: list,
) -> np.ndarray:
    """
    Отрисовывает рамки найденных товаров и пустых мест.
    Возвращает BGR изображение.
    """
    h, w = img_bgr.shape[:2]
    pil = Image.fromarray(cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil, "RGBA")

    # Товары (синие/оранжевые)
    for (x1, y1, x2, y2), label in zip(product_boxes, product_labels):
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        draw.rectangle([x1, y1, x2, y2], outline=COLOR_PRODUCT, width=2)
        bb = draw.textbbox((0, 0), label, font=FONT_SMALL)
        tw, th = bb[2]-bb[0], bb[3]-bb[1]
        ty = max(y1 - th - 6, 0)
        draw.rectangle([x1, ty, x1+tw+8, ty+th+6], fill=(*COLOR_PRODUCT, 200))
        draw.text((x1+4, ty+3), label, font=FONT_SMALL, fill=(255, 255, 255))

    # Пустые места (зелёные)
    for (x1, y1, x2, y2), conf in zip(void_boxes, void_confs):
        x1, y1, x2, y2 = (max(0, int(v)) for v in (x1, y1, x2, y2))
        x2 = min(x2, w-1); y2 = min(y2, h-1)
        draw.rectangle([x1, y1, x2, y2], fill=(*COLOR_VOID, 40))
        draw.rectangle([x1, y1, x2, y2], outline=COLOR_VOID, width=3)
        label = f"{LABEL_VOID_RU} {conf:.0%}"
        bb = draw.textbbox((0, 0), label, font=FONT_LARGE)
        tw, th = bb[2]-bb[0], bb[3]-bb[1]
        ty = max(y1 - th - 8, 0)
        draw.rectangle([x1, ty, x1+tw+10, ty+th+8], fill=(0, 0, 0, 200))
        draw.text((x1+5, ty+4), label, font=FONT_LARGE, fill=COLOR_VOID)

    # Итоговая строка
    summary = f"Товаров: {len(product_boxes)}   Пустых мест: {len(void_boxes)}"
    bb = draw.textbbox((0, 0), summary, font=FONT_LARGE)
    tw, th = bb[2]-bb[0], bb[3]-bb[1]
    draw.rectangle([6, 6, tw+16, th+14], fill=(0, 0, 0, 180))
    draw.text((11, 10), summary, font=FONT_LARGE, fill=(255, 255, 0))

    return cv2.cvtColor(np.array(pil), cv2.COLOR_RGB2BGR)