from aiogram import Router, types, F
from bot.keyboards import get_phone_kb
from database import get_session
from database.crud import UserCRUD

router = Router()


# 🔹 Старт — просим номер
@router.message(F.text == "/start")
async def request_phone(message: types.Message):
    await message.answer(
        "📱 Для работы с ботом отправьте ваш номер телефона:",
        reply_markup=get_phone_kb()
    )


# 🔹 Получение контакта
@router.message(F.contact)
async def handle_contact(message: types.Message):
    contact = message.contact

    # ⚠️ защита: пользователь должен отправить СВОЙ номер
    if contact.user_id != message.from_user.id:
        await message.answer("❌ Отправьте свой номер через кнопку")
        return

    db = get_session()

    user = UserCRUD.create_or_update_user(
        db,
        telegram_id=message.from_user.id,
        phone_number=contact.phone_number
    )

    await message.answer(
        "✅ Регистрация завершена! Теперь можете отправлять фото 📷"
    )
    await message.answer("Введите ID магазина (например: 1):")

@router.message()
async def set_store(message: types.Message):
    if message.text.isdigit():
        db = get_session()
        UserCRUD.set_user_store(
            db,
            telegram_id=message.from_user.id,
            store_id=int(message.text)
        )
        await message.answer("✅ Магазин привязан!")