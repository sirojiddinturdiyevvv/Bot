from loader import dp,bot
from aiogram import types,suppress,html
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram import F
from keyboards.inline.buttons import *
from api import *
from checktest import *
from environs import Env
env =Env()
env.read_env()
url= env.str('URL')
numbers_icon = {
    1:'1️⃣',
    2:'2️⃣',
    3:'3️⃣',
    4:'4️⃣',
    5:'5️⃣'
}
from aiogram.fsm.context import FSMContext
# Command for get test(category)
@dp.message(Command('test'))
async def test(message:types.Message,state:FSMContext):
    try:
            telegram_id = message.from_user.id
            daily_test = dailytest(telegram_id=telegram_id)
            if daily_test == 400:
                await message.answer("Sizga kunlik jami <b>3</b> ta test test beriladi!\n"
                                     "Siz limitdan foydalanib bo'ldiz!")
            else:

                if categories():
                    results = categories()
                    await state.update_data({
                        'data': results
                    })
                    length = len(results)
                    if results:
                        page = 0
                        next = (page + 1) * page_size if length > (page + 1) * page_size else length
                        text1 = f"Natijalar 1-{next} {length} dan\n"
                        text2 = ''
                        counter = 1
                        for i in results[page:next]:
                            text2 += f"{numbers_icon.get(counter)}.{html.bold(i['name'])}" + '\n'
                            counter += 1
                        text1 += '\n' + text2
                        await message.answer(text=text1, reply_markup=pagination_btn(data=results, page=page))
                else:
                    await message.answer("Hali kategoriya va test qo'shilmagan!")
    except Exception as e:
        print(e)
        pass
@dp.callback_query(PaginatorCallback.filter())
async def change_size(call:types.CallbackQuery,callback_data:PaginatorCallback,state:FSMContext):
    page = int(callback_data.page)
    action = callback_data.action
    length  = int(callback_data.length)
    data = await state.get_data()
    results = data['data']
    if action=='delete':
        await call.message.delete()
    else:
        if action == 'next':
            if (page + 1) * page_size >= length:
                await call.answer("Eng oxirgi sahifadasiz...")
                page = page
            else:
                page = page + 1
        else:
            if page > 0:
                page = page - 1
            else:
                await call.answer("Eng oldingi sahifadasiz...")
                page = page
        start = page * page_size
        start_t = (page + 1) if page <= 0 else page * page_size
        finish = (page + 1) * page_size if length > (page + 1) * page_size else length
        text1 = f"Natijalar {start_t}-{finish} {length} dan\n"
        text2 = ''
        counter = 1
        for i in results[start:finish]:
            text2 += f"{numbers_icon.get(counter)}.{html.bold(i['name'])}" + '\n'
            counter += 1
        text1 += '\n' + text2
        with suppress(TelegramBadRequest):
            await call.message.edit_text(text=text1, reply_markup=pagination_btn(data=results, page=page))
# filter for category
@dp.callback_query(CategoryCallBack.filter())
async def chooose_test(call:types.CallbackQuery,callback_data:CategoryCallBack,state:FSMContext):
    try:
        telegram_id = call.from_user.id
        category = int(callback_data.id)
        info = get_test(category=category, telegram_id=telegram_id)
        if info !=[]:
            await call.answer("Tayyorlanmoqda")
            if info == '404':
                await call.message.answer("😐 Uzr bu kategoriya bo'yicha test endi tayyorlanmoqda!\n"
                                          "Yoki bu kategoriyadagi barcha testlarni ishlagansiz!")
                await call.message.delete()
            else:
                black = '◼️'
                white = '◻️'
                xabar = await bot.send_message(chat_id=call.from_user.id, text=10 * white)
                for i in range(1, 11):
                    oq = (10 - i) * white
                    qora = i * black
                    await xabar.edit_text(text=f"{qora}{oq}\n"
                                               f"{i * 10} % tayyorlandi!")
                await xabar.delete()
                await bot.send_chat_action(chat_id=call.from_user.id, action='upload_document')
                text = f"ℹ️ Test kodi : <b>{info['code']}</b>\n" \
                       f"🕐 Test tayyorlangan vaqt : {info['uploaded']}\n" \
                       f"🔄 Test o'zgartirilgan vaqt: {info['changed']}\n" \
                       f"🔢 Test soni: {len(info['answers'])}\n" \
                       f"📌 Kategoriya: {info['category']}\n" \
                       f"🗂 Fayl hajmi: {info['filesize']}\n\n\n" \
                       f"⚠️ Testni tekshirish uchun Test javoblarni quyidagicha yuboring!\n\n" \
                       f"<b>##test_kodi##1a2b3c4d......28d29b30a</b>\n" \
                       f"<b>Masalan:##1002##1a2b3c4d......28d29b30a</b>"
                data = {}
                data[info['code']] = info['answers']
                await state.update_data({
                    f"test": data
                })
                dailytestcreate(telegram_id=call.from_user.id,test_code=info['code'])
                file = info['file']
                file_name = file[file.rfind('/')+1:]
                myfile = types.input_file.URLInputFile(url=url + info['file'],filename=file_name)
                await call.message.answer_document(document=myfile, caption=text,
                                                   reply_markup=start_doing_test(test_code=info['code']),protect_content=True)
            await call.message.delete()
        else:
            await call.answer("Tayyorlanmoqda")
            await call.message.answer("😐 Uzr bu kategoriya bo'yicha test endi tayyorlanmoqda!\n"
                                      "Yoki bu kategoriyadagi barcha testlarni ishlagansiz!")
            await call.message.delete()
    except:
        pass

# Check Answers With Write by Hand
@dp.message(F.text.startswith('#'))
async def checkmytest(message:types.Message,state:FSMContext):
    try:
        answers = message.text
        stuanswers = checkformat(answers)
        if stuanswers:
            test = stuanswers['test']
            answers = stuanswers['answers']
            data = await state.get_data()
            trueanswers = data.get('test', {})
            trueanswers = trueanswers.get(test, None)
            if trueanswers == None:
                await message.answer('<b>😐 Uzr bu kodli test sizga berilmagan!!</b>')
            else:

                result = check(answers=answers, trueanswers=trueanswers)
                score = float(result['score'])

                test_done(telegram_id=message.from_user.id, name=message.from_user.full_name, test_code=test,
                          true_answers=result['trues'], false_answers=result['falses'])
                await message.answer(f"<b>‼️ Test kodi: {test}</b>\n\n{result['result']}")

        else:
            await message.answer(error)
        await state.clear()
    except:
        await state.clear()
# Run After Click "Testni tekshirish"
@dp.callback_query(CheckToCallBack.filter())
async def test(call:types.CallbackQuery,callback_data:CheckToCallBack,state:FSMContext):
    try:
        await call.answer(cache_time=60)
        await call.message.answer("<b>To'g'ri javoblarni belgilang!</b>",
                                  reply_markup=checkbuttonpart_1(test_code=callback_data.test_code))
        await call.message.delete()
    except Exception as e:
        print(e)
        pass
# Run When "Orqaga" or "Oldinga"
@dp.callback_query(NextPreviousCallBack.filter())
async def test(call:types.CallbackQuery,callback_data:NextPreviousCallBack,state:FSMContext):
   try:
       action = callback_data.action
       test_code = callback_data.test_code
       data = await state.get_data()
       answers = data.get(test_code, None)
       if action == 'next':
           await call.message.edit_reply_markup(reply_markup=checkbuttonpart_2(test_code=test_code, answers=answers))
       else:
           await call.message.edit_reply_markup(reply_markup=checkbuttonpart_1(test_code=test_code, answers=answers))
   except:
       pass
# Select clicked answers
@dp.callback_query(CheckCallBack.filter())
async def write(call:types.CallbackQuery,callback_data:CheckCallBack,state:FSMContext):
    try:
        await call.answer("Javob qabul qilindi!")
        test_code = callback_data.test_code
        answer_number = callback_data.answer_number
        answer = callback_data.answer
        data = await state.get_data()
        answers = data.get(test_code, {})
        answers[answer_number] = answer
        await state.update_data({
            test_code: answers
        })
        if int(answer_number) < 16:
            await call.message.edit_reply_markup(reply_markup=checkbuttonpart_1(test_code=test_code, answers=answers))
        else:
            await call.message.edit_reply_markup(
                reply_markup=checkbuttonpart_2(test_code=test_code, answers=answers))
    except:
        pass
# Run after click 'Tugatish'
@dp.callback_query(FinishCallBack.filter())
async def callme(call:types.CallbackQuery,state:FSMContext,callback_data:FinishCallBack):
    try:
        test_code = callback_data.test_code
        data = await state.get_data()
        answers = data.get(test_code, None)
        trueanswers = data.get('test', {})
        trueanswers = trueanswers.get(test_code, None)
        if trueanswers is None:
            await call.answer('Javoblar kiritilmagan!')
        if answers is None:
            await call.answer('Javoblar kiritilmagan!')
        else:
            await call.answer(cache_time=60)
            result = check(trueanswers=trueanswers, answers=answers)

            test_done(telegram_id=call.from_user.id, name=call.from_user.full_name, test_code=test_code,
                      true_answers=result['trues'], false_answers=result['falses'])
            await call.message.answer(f"<b>‼️ Test kodi: {test_code}</b>\n\n{result['result']}")

            await state.update_data({
                test_code: {}
            })
            await call.message.delete()
    except:
        pass
