from aiogram import executor
import logging
from config import dp
from handlers import callback, commands, extra, admin, fsm_mentor


fsm_mentor.register_hanlers_fsm_mentor(dp)
admin.register_handlers_admin(dp)
callback.register_handlers_callback(dp)
commands.register_handlers_commands(dp)
admin.register_handlers_admin_game(dp)

extra.register_handlers_extra(dp)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp)
