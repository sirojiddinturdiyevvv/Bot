from api import categories
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
class Format(CallbackData,prefix='ikb0000'):
    choose:str
class CheckToCallBack(CallbackData,prefix='ikb0002'):
    test_code:str
class FinishCallBack(CallbackData,prefix='ikb0003'):
    test_code:str

class CheckCallBack(CallbackData,prefix='ikb0004'):
    test_code:str
    answer_number:int
    answer:str
class NextPreviousCallBack(CallbackData,prefix='ikb0005'):
    action:str
    test_code:str
# Button for regenarate
def start_doing_test(test_code):
    btn = InlineKeyboardBuilder()
    btn.button(text="📝 Testni tekshirish",callback_data=CheckToCallBack(test_code=test_code))
    btn.adjust(1)
    return btn.as_markup()
# Buttot for check (1-15)
def checkbuttonpart_1(test_code,answers:dict=None):
    btn = InlineKeyboardBuilder()
    for i in range(1,16):
                if answers is  None:
                    answer=None
                else:
                    answer = answers.get(int(i))
                try:

                    btn.row(
                        InlineKeyboardButton(text=f"{i}", callback_data='1'),
                        InlineKeyboardButton(text="✅ A" if answer == "A" else "A",
                                             callback_data=CheckCallBack(test_code=test_code, answer_number=i,
                                                                         answer="A").pack()),
                        InlineKeyboardButton(text="✅ B" if answer == "B" else "B",
                                             callback_data=CheckCallBack(test_code=test_code,
                                                                         answer_number=i, answer="B").pack()),
                        InlineKeyboardButton(text="✅ C" if answer == "C" else "C",
                                             callback_data=CheckCallBack(test_code=test_code, answer_number=i,
                                                                         answer="C").pack()),
                        InlineKeyboardButton(text="✅ D" if answer == "D" else "D",
                                             callback_data=CheckCallBack(test_code=test_code,
                                                                         answer_number=i, answer="D").pack()),
                        width=5

                    )
                except Exception as e:
                    print(e)
    # btn.adjust(5)
    btn.row(
        InlineKeyboardButton(text="➡️ Oldinga", callback_data=NextPreviousCallBack(action='next', test_code=test_code).pack())
    )
    return btn.as_markup()
# Buttot for check (16-30)
def checkbuttonpart_2(test_code,answers=None):
    btn = InlineKeyboardBuilder()
    for i in range(16,31):
        if answers is None:
            answer = None
        else:
            answer = answers.get(int(i))
        try:

            btn.row(
                InlineKeyboardButton(text=f"{i}", callback_data='1'),
                InlineKeyboardButton(text="✅ A" if answer == "A" else "A",
                                     callback_data=CheckCallBack(test_code=test_code, answer_number=i,
                                                                 answer="A").pack()),
                InlineKeyboardButton(text="✅ B" if answer == "B" else "B",
                                     callback_data=CheckCallBack(test_code=test_code,
                                                                 answer_number=i, answer="B").pack()),
                InlineKeyboardButton(text="✅ C" if answer == "C" else "C",
                                     callback_data=CheckCallBack(test_code=test_code, answer_number=i,
                                                                 answer="C").pack()),
                InlineKeyboardButton(text="✅ D" if answer == "D" else "D",
                                     callback_data=CheckCallBack(test_code=test_code,
                                                                 answer_number=i, answer="D").pack()),
                width=5

            )
        except Exception as e:
            print(e)
    btn.row(
       InlineKeyboardButton(text="⬅️ Orqaga", callback_data=NextPreviousCallBack(action='previous', test_code=test_code).pack())
    )
    btn.row(
        InlineKeyboardButton(text="🏁 Tugatish",callback_data=FinishCallBack(test_code=test_code).pack())
    )
    return btn.as_markup()

def text_format(choose=None):
    choose = 'TEXT' if choose==None else choose
    btn  = InlineKeyboardBuilder()
    btn.button(text=f"Markup format: {choose}",callback_data=Format(choose=choose))
    return btn.as_markup()
class CategoryCallBack(CallbackData,prefix='category'):
    id:str
class PaginatorCallback(CallbackData,prefix='page'):
    action:str
    page:int
    length:int
page_size=5
def pagination_btn(data,page:int=0):
    btn = InlineKeyboardBuilder()
    length = len(data)
    data = data
    try:
        start = page * page_size
        finish = (page + 1) * page_size
        if finish > length:
            datas = data[start:length]
        else:
            datas = data[start:finish]
    except:
        pass
    counter = 1
    for i in datas:
        btn.row(
            InlineKeyboardButton(text=f"{counter}", callback_data=CategoryCallBack(id=str(i['id'])).pack()),
            width=5
        )
        counter+=1
    btn.adjust(len(datas))
    btn.row(
        InlineKeyboardButton(text='⬅️',
                             callback_data=PaginatorCallback(action='prev', page=page, length=length).pack()),
        InlineKeyboardButton(text='❌',
                             callback_data=PaginatorCallback(action='delete', page=page, length=length).pack()),
        InlineKeyboardButton(text='➡️', callback_data=PaginatorCallback(action='next', page=page, length=length).pack())
    )
    return btn.as_markup()