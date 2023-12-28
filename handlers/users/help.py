from aiogram import types
from aiogram.filters import Command
from loader import dp
from api import delete_done_test
@dp.message(Command('help'))
async def bot_help(message: types.Message):
    text = ("Buyruqlar: ",
            "/start - Botni ishga tushirish",
            "/help - Yordam",
            "/info - Ma'lumot",
            "/test - Test olish",
            "/reset - Barcha oldingi natijalarni o'chirish",)
    await message.answer("\n".join(text))
@dp.message(Command('reset'))
async def bot_help(message: types.Message):
    try:
        delete_done_test(message.from_user.id)
    except:
        pass
    await message.answer("Barcha natijalar o'chirildi!!!")
