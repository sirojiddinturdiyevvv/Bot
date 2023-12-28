from aiogram import types
from loader import dp
@dp.message()
async def default(message: types.Message):
    await message.answer("Tushunarsiz buyruq!")

