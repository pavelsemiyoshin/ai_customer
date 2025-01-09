
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import config
import database

api = config.API
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

import handlers.Start
import handlers.Admin
import handlers.Lessions


dp.message_handler(lambda m: database.check_block(m.from_user.id))(handlers.Start.ban_message)
dp.callback_query_handler(lambda c: database.check_block(c.from_user.id))(handlers.Start.ban_callbackquery)

dp.message_handler(commands=['start'])(handlers.Start.start)
dp.callback_query_handler(text='start_case')(lambda message, state: handlers.Start.start_case(message, state))
dp.callback_query_handler(text='stop_case', state=handlers.Start.DialogState.active)(lambda message, state: handlers.Start.stop_case(message, state))
dp.callback_query_handler(text='stop_case', state=handlers.Start.DialogState.success)(lambda message, state: handlers.Start.stop_case(message, state))
dp.callback_query_handler(text='show_saleplan', state=handlers.Start.DialogState.active)(lambda message, state: handlers.Start.show_saleplan(message, state))

dp.message_handler(content_types=types.ContentTypes.VOICE, state=handlers.Start.DialogState.active)(lambda message, state: handlers.Start.user_voice(message, state, bot))

dp.message_handler(Text(equals=['👀 Учить скрипты']))(handlers.Start.lessions)

dp.message_handler(Text(equals=['Убрать клавиатуру']))(handlers.Start.remove_keyboard)

dp.message_handler(commands=['admin'])(handlers.Admin.start)
dp.callback_query_handler(text="statistick")(handlers.Admin.statistick)
dp.callback_query_handler(text="users")(handlers.Admin.users)
dp.callback_query_handler(text="mailing")(handlers.Admin.mailing)
dp.message_handler(state=handlers.Admin.admins.mailing_step1)(handlers.Admin.mailing1)
dp.message_handler(content_types=types.ContentTypes.PHOTO, state=handlers.Admin.admins.mailing_step2)(handlers.Admin.mailing2)
dp.callback_query_handler(text="block")(handlers.Admin.block)
dp.message_handler(state=handlers.Admin.admins.ban)(handlers.Admin.ban1)
dp.callback_query_handler(text="back_to_admin")(handlers.Admin.back_admin)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates = True)