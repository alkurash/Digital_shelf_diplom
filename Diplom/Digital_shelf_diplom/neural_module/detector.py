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

import torch
from ultralytics import YOLO
import numpy as np

# ── Патч совместимости torch.load (из твоего кода) ──
_orig_torch_load = torch.load
def _patched_torch_load(*args, **kwargs):
    kwargs['weights_only'] = False
    return _orig_torch_load(*args, **kwargs)
torch.load = _patched_torch_load

class RetailDetector:
    def __init__(self, weights_all_path: str, weights_void_path: str):
        self.conf_all = 0.15
        self.conf_void = 0.1
        
        # Загрузка модели товаров
        try:
            self.model_all = YOLO(weights_all_path)
        except Exception as e:
            print(f"Ошибка загрузки best_2.pt: {e}")
            self.model_all = None

        # Загрузка модели пустых мест
        try:
            self.model_void = YOLO(weights_void_path)
        except Exception as e:
            print(f"Ошибка загрузки shelf_void_detector.pt: {e}")
            self.model_void = None

    def detect(self, img_bgr: np.ndarray) -> dict:
        """
        Принимает изображение (numpy array BGR), возвращает словари с боксами и позициями.
        """
        img_h, img_w = img_bgr.shape[:2]
        
        product_boxes, product_labels = [], []
        void_boxes, void_confs, void_positions = [], [], []

        # Детекция товаров
        if self.model_all:
            res_all = self.model_all.predict(img_bgr, conf=self.conf_all, verbose=False)[0]
            for box, cls_id in zip(res_all.boxes.xyxy.cpu().numpy(), res_all.boxes.cls.cpu().numpy().astype(int)):
                product_boxes.append(box.tolist())
                product_labels.append(self.model_all.names.get(cls_id, str(cls_id)))

        # Детекция пустых мест
        if self.model_void:
            res_void = self.model_void.predict(img_bgr, conf=self.conf_void, verbose=False)[0]
            if len(res_void.boxes):
                void_boxes = res_void.boxes.xyxy.cpu().numpy().tolist()
                void_confs = res_void.boxes.conf.cpu().numpy().tolist()

                # Вычисление позиций пустых мест для LLM
                for (x1, y1, x2, y2) in void_boxes:
                    cx = (x1 + x2) / 2 / img_w
                    cy = (y1 + y2) / 2 / img_h
                    bw = (x2 - x1) / img_w
                    bh = (y2 - y1) / img_h
                    hz = "левая" if cx < 0.33 else ("центральная" if cx < 0.67 else "правая")
                    vz = "верхняя" if cy < 0.33 else ("средняя" if cy < 0.67 else "нижняя")
                    void_positions.append(f"{hz} {vz} часть полки (ш={bw:.0%}, в={bh:.0%})")

        return {
            "products": {
                "boxes": product_boxes,
                "labels": product_labels,
                "count": len(product_boxes)
            },
            "voids": {
                "boxes": void_boxes,
                "confs": void_confs,
                "positions": void_positions,
                "count": len(void_boxes)
            }
        }