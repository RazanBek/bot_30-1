from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import ADMINS
from . import keyboards


class FSMAdmin(StatesGroup):
    name = State()
    age = State()
    gender = State()
    napravlenie = State()
    group = State()
    photo = State()
    submit = State()


async def fsm_start(message: types.Message):
    if message.chat.type == 'private' and message.from_user.id in ADMINS:
        await FSMAdmin.name.set()
        await message.answer("Как зовут ментора?", reply_markup=keyboards.cancel_markup)
    else:
        await message.reply("Пишите в личке!")


async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMAdmin.next()
    await message.answer("Сколько лет ментору?", reply_markup=keyboards.cancel_markup)


async def load_age(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Пишите числа!")
    elif not 10 < int(message.text) < 66:
        await message.answer("Не соответствует возрастному ограничению!")
    else:
        async with state.proxy() as data:
            data['age'] = message.text
        await FSMAdmin.next()
        await message.answer("Какой у ментора пол?", reply_markup=keyboards.gender_markup)


async def load_gender(message: types.Message, state: FSMContext):
    if message.text.lower() not in ['женщина', 'мужчина']:
        await message.answer("Пользуйтесь кнопками!")
    else:
        async with state.proxy() as data:
            data['gender'] = message.text
        await FSMAdmin.next()
        await message.answer("Какое направление у ментора?", reply_markup=keyboards.cancel_markup)


async def load_napravlenie(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['napravlenie'] = message.text
    await FSMAdmin.next()
    await message.answer("Введите номер группы", reply_markup=keyboards.cancel_markup)


async def load_group(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['group'] = message.text
    await FSMAdmin.next()
    await message.answer("отправьте фото ментора", reply_markup=keyboards.cancel_markup)


async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
        await message.answer_photo(data['photo'],
                                   caption=f"Имя ментора:{data['name']}\n"
                                           f"Возраст:{data['age']}\n"
                                   f"Пол:{data['gender']}\n"
                                           f"Направление: {data['napravlenie']}"
                                   f"_{data['group']}")
    await FSMAdmin.next()
    await message.answer("Все верно?", reply_markup=keyboards.submit_markup)


async def submit(message: types.Message, state: FSMContext):
    if message.text.lower() == 'да':
        # TODO: Запись в БД
        await state.finish()
        await message.answer("Записал в БД!")
    elif message.text.lower() == 'заново':
        await FSMAdmin.name.set()
        await message.answer("Как зовут ментора?", reply_markup=keyboards.cancel_markup)
    else:
        await message.answer("Используйте кнопки!")


async def cancel_reg(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
        await message.answer("До скорых встреч!")
    else:
        await message.answer("Что ты отменяешь?!")


def register_hanlers_fsm_mentor(dp: Dispatcher):
    dp.register_message_handler(cancel_reg, commands=['cancel'], state='*')
    dp.register_message_handler(cancel_reg, Text(equals="отмена", ignore_case=True), state='*')

    dp.register_message_handler(fsm_start, commands=['reg'])
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_age, state=FSMAdmin.age)
    dp.register_message_handler(load_gender, state=FSMAdmin.gender)
    dp.register_message_handler(load_napravlenie, state=FSMAdmin.napravlenie)
    dp.register_message_handler(load_group, state=FSMAdmin.group)
    dp.register_message_handler(load_photo, state=FSMAdmin.photo,
                                content_types=['photo'])
    dp.register_message_handler(submit, state=FSMAdmin.submit)
