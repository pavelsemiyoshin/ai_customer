from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo


# start_kb = ReplyKeyboardMarkup(
#     keyboard=[
#         [
#             KeyboardButton(text = '✅ Пройти кейс'),
#             KeyboardButton(text = '👀 Учить скрипты')
#         ],
#     ],resize_keyboard=True
# )

start_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text = '✅ Пройти кейс', callback_data = 'start_case'),
        ],
    ]
)

stop_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text = '👀 Подсказка', callback_data = 'show_saleplan'),
            InlineKeyboardButton(text = '🚫 Закончить', callback_data = 'stop_case'),
        ],
    ]
)


catalog_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text = 'Маникюр', callback_data = 'Маникюр'),
        ],
        [
            InlineKeyboardButton(text = 'Педикюр', callback_data = 'Педикюр'),
        ],
        [
            InlineKeyboardButton(text = 'Наращивание', callback_data = 'Наращивание'),
        ],
        [
            InlineKeyboardButton(text = 'Другие предложения', callback_data = 'Другие предложения'),
        ],
    ]
)


buy_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🛍 Купить", url = "https://t.me/jlosos1856"),
        ],
        [
            InlineKeyboardButton(text="🔙 Назад", callback_data = "back_to_preiskurant"),
        ],
    ]
)


AdminPanel = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="👥 Пользователи", callback_data = "users"),
        ],
        [
            InlineKeyboardButton(text="📊 Статистика", callback_data = "statistick"),
        ],
        [
            InlineKeyboardButton(text="✉️ Рассылка", callback_data = "mailing"),
        ],
        [
            InlineKeyboardButton(text="❌ Блокировка", callback_data = "block"),
        ],
    ]
)

back_to_admin = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🔙 Назад", callback_data = "back_to_admin"),
        ],
    ]
)

start_lessions_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🛍 Скрипты продаж", callback_data = "scripts"),#url = "https://t.me/jlosos1856"),
        ],
        [
            #InlineKeyboardButton(text="Скрипты по продукции Berger", url = "https://drive.google.com/file/d/1F_KUcctqa955MK5AK2eAk_kR2JbQDR9m/view?usp=sharing"), #callback_data = "berger"),
            #InlineKeyboardButton(text="Скрипты по продукции Berger",web_app=WebAppInfo(url="https://t.me/iv?url=https://telegra.ph/vy-12-07-2&rhash=6bbd1dcdbe351a")),
            InlineKeyboardButton(text="Скрипты по продукции Berger",web_app=WebAppInfo(url="https://jlkourse.tilda.ws/")),
        ],
        [
            InlineKeyboardButton(text="Скрипты по продукции Berger",web_app=WebAppInfo(url="https://jlkourse.tilda.ws/berger_tech")),
        ],
    ]
)
