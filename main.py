from aiogram import Bot, Dispatcher, types, executor
import random
from decouple import config
import logging
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = config("TOKEN")
bot = Bot(TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['mem'])
async def command_start(message: types.Message):
    photos = [
        'media/мем.jpg',
        'media/мем1.jpg',
        'media/мем2.jpg',
        'media/мем3.jpg',
    ]
    photo = open(random.choice(photos), 'rb')
    await bot.send_photo(message.from_user.id, photo)


@dp.message_handler(commands=['quiz'])
async def quiz_1(message: types.message) -> None:
    markup= InlineKeyboardMarkup()
    next_buttun = InlineKeyboardButton("NEXT", callback_data="next_button_1")
    markup.add(next_buttun)

    quiestion = "да или нет"
    answers = [
        'да',
        'нет',
    ]
    await message.answer_poll(
        question=quiestion,
        options=answers,
        is_anonymous=False,
        type='quiz',
        correct_option_id=1,
        reply_markup=markup
    )


@dp.callback_query_handler(text="next_button_1")
async def quiz_2(callback: types.CallbackQuery):
    quiestion = "2 + 2 = 5"
    answers = [
        'да',
        'нет',
    ]
    await callback.message.answer_poll(
        question=quiestion,
        options=answers,
        is_anonymous=False,
        type='quiz',
        correct_option_id=1,
    )


@dp.message_handler(content_types=['text'])
async def echo(message: types.Message):
    if message.text.isnumeric():
        await message.answer(int(message.text) ** 2)
    else:
        await bot.send_message(message.from_user.id, message.text)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp)
