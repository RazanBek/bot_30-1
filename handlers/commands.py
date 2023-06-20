from aiogram import types, Dispatcher
import random
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import bot, dp, ADMINS


async def command_mem(message: types.Message):
    photos = [
        'media/мем.jpg',
        'media/мем1.jpg',
        'media/мем2.jpg',
        'media/мем3.jpg',
    ]
    photo = open(random.choice(photos), 'rb')
    await bot.send_photo(message.from_user.id, photo)


async def quiz_1(message: types.message) -> None:
    markup = InlineKeyboardMarkup()
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


async def pin(message: types.Message):
    if message.reply_to_message:
        await bot.pin_chat_message(message.chat.id, message.message_id)


def register_handlers_commands(dp: Dispatcher):
    dp.register_message_handler(command_mem, commands=['mem'])
    dp.register_message_handler(quiz_1, commands=['quiz'])
    dp.register_message_handler(pin, commands=['pin'], commands_prefix='!/')
