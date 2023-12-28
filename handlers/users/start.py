import logging
from aiogram import types
from aiogram.filters import Command
from loader import bot, dp
from api import *
# Start Command
@dp.message(Command('start'))
async def show_channels(message: types.Message):
    user = message.from_user.id
    create_user(telegram_id=user,name=message.from_user.full_name)
    try:
        id = "CgACAgIAAxkDAANaZReo_O6ZVLqcA6yak_csD9Ony1oAAqAvAAIyesFIoLzhpdd6jR0wBA"
        await message.answer_animation(animation=id, caption='Qani bilimdon,Testni boshlaymizmi?!')
        await message.answer(f"<b>Assalomu alaykum {message.from_user.full_name} botimizga xush kelibsiz!</b>\n"
                             f"<i>Test ishlash uchun /test buyrug'ini bosing!</i>\n\n\n"
                             f"<b><u>Muammo bo'lsa /info buyrug'idan kerakli malumotni bilib oling</u></b>")
    except:
        await message.answer(f"<b>Assalomu alaykum {message.from_user.full_name} botimizga xush kelibsiz!</b>\n"
                             f"<i>Test ishlash uchun /test buyrug'ini bosing!</i>\n\n\n"
                             f"<b><u>Muammo bo'lsa /info buyrug'idan kerakli malumotni bilib oling</u></b>")

