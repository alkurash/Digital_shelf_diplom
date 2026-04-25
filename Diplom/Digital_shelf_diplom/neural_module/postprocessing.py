# Цель: Генерация аннотированных изображений
# Методы:

# draw_bboxes(image, detections, color_scheme) - отрисовка боксов
# add_labels(image, detections, font_size) - добавление меток классов
# highlight_violations(image, violations) - выделение нарушений красным
# add_compliance_badge(image, compliance_score) - бейдж с % соответствия
# create_side_by_side_view(original, annotated, planogram) - сравнение
# add_legend(image, classes) - легенда по цветам
# save_annotated_image(image, output_path) - сохранение результата