from loader import dp,bot
from aiogram import types,html
from api import results_of_test
from telegraph.aio import Telegraph
from aiogram.filters import Command
async def create_mypage(data,title):
    telegraph = Telegraph()
    await telegraph.create_account(short_name='2305')
    response = await telegraph.create_page(
        title=title,
        html_content=data,
    )
    return response['url']

@dp.message(Command('info'))
async def test(message:types.Message):
    await message.answer(f"<b>Test tekshirishda agar tugmalar orqali belgilaganda muammo chiqsa,Yozma holda kiriting!</b>\n"
                         f"<i>Hozirda kamchiliklar tuzatilmoqda!</i>")
@dp.message(Command('results'))
async def test(message:types.Message):
    try:
            await bot.send_chat_action(chat_id=message.chat.id, action='typing')
            user = message.from_user.id
            data = results_of_test(telegram_id=user)
            if data == []:

                await message.answer(f"{html.bold('Siz hali test ishlamapsiz!!!')}\n"
                                     f"<i>Test ishlash uchun /test buyrug'ini bosing!\n\n\nMuammo bo'lsa /info buyrug'idan kerakli malumotni bilib oling</i>")
            else:
                text = ''
                for i in data:
                    text += f"<p>Test kodi: <b>{i['test_code']}</b>.✅ To'g'ri javoblar: <b>{i['true_answers']}</b>.❌ Xato javoblar: <b>{i['false_answers']}</b>.🕐 Bajarilgan vaqt: <b>{i['date']}</b></p>"
                info = await create_mypage(title=f"{message.from_user.full_name} ning jami natijalari!",
                                           data=text)
                await message.answer(f"Malumotni <a href='{info}'>ushbu</a> havola orqali olishingiz mumkin!")

    except Exception as e:
        print(e)


