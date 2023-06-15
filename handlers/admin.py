from aiogram import types, Dispatcher
from config import bot, dp, ADMINS
import random


async def ban(message: types.Message):
    if message.from_user.id in ADMINS and message.reply_to_message:
        await bot.kick_chat_member(message.chat.id, message.message_id)


async def game(message: types.Message):
    if message.text.startswith('game') and message.from_user.id in ADMINS:
        emojis = ['🎯', '🎳', '🎰', '🎲', '⚽', '️🏀']
        rand_game = random.choice(emojis)
        await bot.send_dice(message.chat.id, emoji=rand_game)


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(ban, commands=['ban'], commands_prefix='!/')
    dp.register_message_handler(game)
