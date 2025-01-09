from aiogram.types import InputMediaPhoto

from keyboards import *


async def scripts(message):
    with open('files/media/info.jpg', "rb") as img:
        await message.answer_photo(img, '<b>Выберите интересующую вас информацию</b>', parse_mode='HTML', reply_markup=start_lessions_kb)

#async def berger(message):
#    with open('files/berger/0.png', "rb") as img:
#        await message.answer_photo(img, '<b>Перейти к следующему слайду</b>', parse_mode='HTML', reply_markup=start_lessions_kb)

async def berger(call):
    with open('files/berger/0.png', "rb") as img:
        mes = InputMediaPhoto(media=img, caption=texts.category.manikur, parse_mode='HTML')
        await call.message.edit_media(mes, reply_markup=buy_kb)
    await call.answer()
