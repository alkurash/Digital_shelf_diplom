# Обработка входящих фотографий от мерчендайзера
# Цель: Обработка загрузки фотографий от пользователей
# Методы:

# handle_photo(message: Message) - основной обработчик получения фото
# validate_photo(photo) - проверка формата и качества изображения
# save_temp_photo(photo, user_id) - сохранение фото во временное хранилище
# send_to_neural_module(photo_path) - отправка фото в нейросетевой модуль
# handle_processing_result(result) - обработка результата от нейросети
# send_annotated_image(user_id, image_path) - отправка аннотированного изображения пользователю