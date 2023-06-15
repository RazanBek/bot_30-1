from aiogram import types, Dispatcher
from config import bot, dp, ADMINS
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def quiz_2(call: types.CallbackQuery):
    markup = InlineKeyboardMarkup()
    button_call = InlineKeyboardButton("NEXT", callback_data="button_call_2")
    markup.add(button_call)

    question = "ноут или комп"
    answers = [
        "ноут",
        "комп",
        "не знаю",
    ]
    await bot.send_poll(
        chat_id=call.message.chat.id,
        question=question,
        options=answers,
        is_anonymous=False,
        type='quiz',
        correct_option_id=2,
        reply_markup=markup
    )


async def quiz_3(callback: types.CallbackQuery):
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


def register_handlers_callback(dp: Dispatcher):
    dp.register_callback_query_handler(quiz_2, text="next_button_1")
    dp.register_callback_query_handler(quiz_3, text="button_call_2")