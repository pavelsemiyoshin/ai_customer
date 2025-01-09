import texts.start
from keyboards import *
from aiogram import Bot

from aiogram.dispatcher import FSMContext
import database

import os

from aiogram.types import InputFile
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InputMediaPhoto

import ai

# Переменная для хранения цепочки сообщений
LOG_DIALOG = []

# Состояния для конечного автомата
class DialogState(StatesGroup):
    active = State()
    success = State()
 #   customerdesc = State()
 #   saleplan = State()

async def start(message):
    database.add(message.from_user.id)
    await message.answer(f'✅ Добро пожаловать, @{message.from_user.username}!\n\n' + texts.start.start, parse_mode='HTML', reply_markup=start_kb)

# ---------------------------------------------------------
async def start_case(call, state: FSMContext):
    await call.answer()
    sent_statemessage = await call.message.answer("..готовим сценарий..")
    await state.set_state(DialogState.active)
    # Генерируем описание роли покупателя
    CDESC = ai.generate_customer()
    await state.update_data(customerdesc=CDESC)
    print(f"Описание роли покупателя {CDESC}")

    #Выводим в чат информацию
    await sent_statemessage.delete()
    with open('files/media/lessions0.png', "rb") as img:
        mes = InputMediaPhoto(media=img, caption=f'Вы в роли ПРОДАВЦА. Робот в роли ПОКУПАТЕЛЯ. Начните диалог с приветствия покупателя: запишите голосовое сообщение, удерживая знак микрофона!\n\n'
                                                 f'Описание ПОКУПАТЕЛЯ: {CDESC}', parse_mode='HTML')
        await call.message.edit_media(mes, reply_markup=stop_kb)

    sent_statemessage = await call.message.answer("..вы пока читайте, я еще поготовлюсь..")
    #Определяем сценарий, который считается правильным для продажи этому покупателю
    SPLAN = ai.def_sale_plan(CDESC)
    await state.update_data(saleplan=SPLAN)
    print(f'PLAN: {SPLAN}')
    #Задаем системные настройки контектста диалога с ИИ
    LOG_DIALOG.clear()
    LOG_DIALOG.append(
        {"role": "system",
         "content": f"Ты - покупатель в магазине ювелирных изделий, подходящий под следующее описание: {CDESC}."
                    f"Ты купишь, если продавец сделает шаги, похожие на следующие: {SPLAN}. Если ты согласен сделать покупку, ответь одним словом ""Беру"""}
    )
    await sent_statemessage.delete()
    await call.message.answer(f"Все готово! Можем продолжать: зажмите микрофон и общайтесь с покупателем")
# ---------------------------------------------------------
async def final(state: FSMContext):
    current_state = await state.get_state()
    print(f"Состояние: {current_state}, это успех = {current_state == 'DialogState:success'}")
    if current_state == 'DialogState:success':
        res = f"Поздравляю с успешной продажей!\n"
    else:
        res = f"К сожалению продажа не состоялась :(\n"
    print(LOG_DIALOG)
    data = await state.get_data()
    # получим оценку
    LOG_DIALOG.append(
        {"role": "user",
         "content": f"Оцени от 0 до 10 насколько процесс продажи покупателю соответствует технологии продаж и сценарию: {data.get('saleplan')}"}
    )
    ans = ai.custamer_say(LOG_DIALOG)
    res += ans + f"\n Ожидаемая последовательность действий с таким покупателем:\n{data.get('saleplan')}"

    # Очистка состояния и лога
    await state.finish()
    LOG_DIALOG.clear()

    return res

async def stop_case(call, state: FSMContext):
    await call.message.answer("Диалог завершен")
    res = await final(state)
    await call.message.answer(f'{res}')
    await call.message.answer(f'\n\n✅ Готовы пройти еще один кейс?\n', parse_mode='HTML', reply_markup=start_kb)

# ---------------------------------------------------------
async def user_voice(message, state: FSMContext, bot: Bot):
    statusmess = await message.answer("..обрабатываю..")
    file_id = message.voice.file_id                         # Получаем файл голосового сообщения
    audio_file = await bot.download_file_by_id(file_id)     # Скачиваем файл голосового сообщения

    userid = message.from_user.id
    audio_file_path = f"voice_{userid}.ogg"
    print(audio_file_path)
    with open(audio_file_path, 'wb') as f:
        f.write(audio_file.getvalue())                      # Сохраняем файл

    transcript = ai.audio_to_text(audio_file_path,userid)   # преобразуем в текст
    await message.answer(f"Вы сказали: \n{transcript}")
    await statusmess.delete()

    statusmess = await message.answer("..думаю, готовлю ответ..")
    #Генерируем ответ через GPT
    #----
    LOG_DIALOG.append(
        {"role": "user",
         "content": f"Продавец тебе сказал: {transcript}. Составьте ответ продавцу"}
    )
    ans = ai.custamer_say(LOG_DIALOG)
    await message.answer(f"ПОКУПАТЕЛЬ:\n\n{ans}....")
    await statusmess.delete()

    statusmess = await message.answer("..записываю голосовое..")
    print(ans)
    LOG_DIALOG.append(
        {"role": "assistant",
         "content": f"{ans}"}
    )
    if 'БЕРУ' in ans.upper():
        await state.set_state(DialogState.success)
    #Преобразуем ответ в аудио
    mp3_file_path = ai.text_to_audio(ans, userid)
    if not os.path.exists(mp3_file_path):
        print(f"Файл не найден: {mp3_file_path}")
        await message.answer(f'Упс... Что то пошло не так: не могу ответить\n', parse_mode='HTML', reply_markup=stop_kb)
    else:
        await message.answer_voice(InputFile(mp3_file_path),reply_markup=stop_kb)
    await statusmess.delete()

    ## Удаляем временные файлы (по желанию)
    os.remove(audio_file_path)
    os.remove(mp3_file_path)

    current_state = await state.get_state()
    print(f"Состояние: {current_state}, это успех = {current_state == 'DialogState:success'}")
    if current_state == 'DialogState:success':
        statusmess = await message.answer("..продажа состоялась, подводим итоги..")
        res = await final(state)
        statusmess.delete()
        await message.answer(f'{res}')
        await message.answer(f'\n\n✅ Готовы пройти еще один кейс?\n', parse_mode='HTML', reply_markup=start_kb)
    else:
        await message.answer(f"Давайте продолжать: зажмите микрофон и продолжайте продавать. Успех уже близко!")

async def show_saleplan(call, state: FSMContext):

    data = await state.get_data()
    print(f"Запрос подсказки:\n {data['saleplan']}")
    if 'saleplan' in data:
        await call.message.answer(f"Ожидаемая последовательность действий с таким покупателем:\n{data['saleplan']}", parse_mode='HTML', reply_markup=stop_kb)
    else:
        await call.message.answer(f"Ожидаемая последовательность действий с таким покупателем не сформирована")
    await call.message.answer(f"Давайте продолжим!\n Зажмите микрофон и общайтесь с покупателем")

async def remove_keyboard(message):
    await message.answer("Клавиатура убрана!", reply_markup=ReplyKeyboardRemove())

async def lessions(message):
    with open('files/media/lessions0.png', "rb") as img:
        await message.answer_photo(img, texts.start.lession_start, parse_mode='HTML', reply_markup=start_lessions_kb)


async def ban_message(update):
    await update.answer(texts.admin.ban, parse_mode='HTML')


async def ban_callbackquery(update):
    await update.message.answer(texts.admin.ban, parse_mode='HTML')
    await update.answer()

