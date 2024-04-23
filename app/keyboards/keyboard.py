from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from app import database as db

main_kb = [
    [KeyboardButton(text="🔎 Поиск объявлений"),
     KeyboardButton(text="💼 Профиль")],
    [KeyboardButton(text="⚙️ Настройки"),
     KeyboardButton(text="ℹ️ Помощь")]
]

admin_kb = [
    [KeyboardButton(text="🔎 Поиск объявлений"),
     KeyboardButton(text="💼 Профиль")],
    [KeyboardButton(text="⚙️ Настройки"),
     KeyboardButton(text="ℹ️ Помощь")],
    [KeyboardButton(text='💻 Админ-Панель')]
]

admin_panel_kb = [
    [KeyboardButton(text='Сделать рассылку'),
     KeyboardButton(text='Редактирование подписок')],
    [KeyboardButton(text='Выслать логи бота'),
     KeyboardButton(text='Управление пользователями')]
]

main = ReplyKeyboardMarkup(keyboard=main_kb, resize_keyboard= True, input_field_placeholder='Выберите пункт ниже')

main_admin = ReplyKeyboardMarkup(keyboard=admin_kb, resize_keyboard=True, input_field_placeholder='Выберите пункт ниже')

admin_panel = ReplyKeyboardMarkup(keyboard=admin_panel_kb, resize_keyboard=True, input_field_placeholder='Выберите пункт ниже')


search_list_kb = [
    [InlineKeyboardButton(text='➡️ DEPOP', callback_data='DEPOP'),
     InlineKeyboardButton(text='➡️ EBAY', callback_data='EBAY')],
    [InlineKeyboardButton(text='➡️ KLEINANZEIGEN', callback_data='KLEINANZEIGEN'),
     InlineKeyboardButton(text='➡️ ETSY', callback_data="ETSY")]
]

search_list = InlineKeyboardMarkup(row_width=2, inline_keyboard=search_list_kb)


klein_list_kb = [
    [InlineKeyboardButton(text='🇩🇪 KLEINANZEIGEN.DE', callback_data='klein')]
]

klein_list = InlineKeyboardMarkup(row_width=2, inline_keyboard=klein_list_kb)


etsy_list_kb = [
    [InlineKeyboardButton(text='🇦🇺 ETSY.AU', callback_data='ETSY_AU'),
     InlineKeyboardButton(text='🇩🇪 ETSY.DE', callback_data='ETSY_DE')],
    [InlineKeyboardButton(text='🇪🇸 ETSY.ES', callback_data='ETSY_ES'),
     InlineKeyboardButton(text='🇫🇷 ETSY.FR', callback_data='ETSY_FR')],
    [InlineKeyboardButton(text='🇭🇺 ETSY.HU', callback_data='ETSY_HU'),
     InlineKeyboardButton(text='🇮🇹 ETSY.IT', callback_data='ETSY_IT')],
    [InlineKeyboardButton(text='🇵🇱 ETSY.PL', callback_data='ETSY_PL'),
     InlineKeyboardButton(text='🇬🇧 ETSY.UK', callback_data='ETSY_UK')]
]

etsy_list = InlineKeyboardMarkup(row_width=2, inline_keyboard=etsy_list_kb)


ebay_list_kb = [
    [InlineKeyboardButton(text='🇩🇪 EBAY.DE', callback_data='EBAY_DE')]
]

ebay_list = InlineKeyboardMarkup(row_width=1, inline_keyboard=ebay_list_kb)

depop_list_kb = [
    [InlineKeyboardButton(text='🇦🇺 DEPOP.COM', callback_data='DEPOP_AU'),
     InlineKeyboardButton(text='🇩🇪 DEPOP.COM', callback_data='DEPOP_DE')],
    [InlineKeyboardButton(text='🇫🇷 DEPOP.COM', callback_data='DEPOP_FR'),
     InlineKeyboardButton(text='🇬🇧 DEPOP.COM', callback_data='DEPOP_GB')],
    [InlineKeyboardButton(text='🇮🇹 DEPOP.COM', callback_data='DEPOP_IT'),
     InlineKeyboardButton(text='🇺🇸 DEPOP.COM', callback_data='DEPOP_US')]
]

depop_list = InlineKeyboardMarkup(row_width=1, inline_keyboard=depop_list_kb)


payment_method_kb = [
    [InlineKeyboardButton(text='⚜️ CryptoBot', callback_data='crypto_bot')],
    [InlineKeyboardButton(text='⬅ Назад', callback_data='back_to_start')]
]

payment_method = InlineKeyboardMarkup(row_width=1, inline_keyboard=payment_method_kb)



back_to_payment_methods_kb = [
    [InlineKeyboardButton(text='⬅ Назад', callback_data="back_to_balance")]
]


back_to_payment_methods = InlineKeyboardMarkup(inline_keyboard=back_to_payment_methods_kb)


settings_kb = [
    [InlineKeyboardButton(text='🛠 Конфигуратор Объявлений', callback_data='configurator')]
]

settings = InlineKeyboardMarkup(row_width=1, inline_keyboard=settings_kb)

profile_kb = [
    [InlineKeyboardButton(text='💰 Пополнить баланс', callback_data='deposit'),
     InlineKeyboardButton(text='✒️ Оформить подписку', callback_data='subscribe')]
]

profile = InlineKeyboardMarkup(row_width=2, inline_keyboard=profile_kb)





klein_after_parsing_kb = [
    [
        InlineKeyboardButton(text="📊 .JSON", callback_data="klein_json"),
        InlineKeyboardButton(text='💬 Сообщения', callback_data="klein_message")
    ],
    [
        InlineKeyboardButton(text="🤖 Авто рассылка", callback_data="klein_send_messages")
    ],
    [
        InlineKeyboardButton(text="📈 Сортировать по дате регистрации", callback_data="seller_date_sorting"),
        InlineKeyboardButton(text="🗑 Удалить товары с рейтингом", callback_data="seller_feedback_delete")
    ],
    [
      InlineKeyboardButton(text="📦 Удалить товары без доставки", callback_data="delete_without_sipping")
    ],
    [
        InlineKeyboardButton(text="Обновить отчет", callback_data="update_parser_status")
    ]
]

klein_after_parsing = InlineKeyboardMarkup(row_width=2, inline_keyboard=klein_after_parsing_kb)


ebay_categories_kb = [
    [
        InlineKeyboardButton(text='🗽 Антиквариат', callback_data='ebay_category|antique'),
        InlineKeyboardButton(text='🚘 Автомобили и мотоциклы', callback_data='ebay_category|transport')
    ],
    [
        InlineKeyboardButton(text='⚙️ Запчасти для автомобилей', callback_data='ebay_category|details'),
        InlineKeyboardButton(text='🍼 Дети и младенцы', callback_data='ebay_category|baby')
    ],
    [
        InlineKeyboardButton(text='🎨 Рукоделие', callback_data='ebay_category|craft'),
        InlineKeyboardButton(text='💅🏻 Красота', callback_data='ebay_category|beauty')
    ],
    [
        InlineKeyboardButton(text='✉️ Марки', callback_data='ebay_category|stamps'),
        InlineKeyboardButton(text='📚 Книги и журналы', callback_data='ebay_category|books')
    ],
    [
        InlineKeyboardButton(text='🖇 Офис и канцтовары', callback_data='ebay_category|office'),
        InlineKeyboardButton(text='📈 Бизнес и промышленность', callback_data='ebay_category|business')
    ],
    [
        InlineKeyboardButton(text='🖥 Компьютеры и сеть', callback_data='ebay_category|computer'),
        InlineKeyboardButton(text='🍇 Гурман или дегустатор', callback_data='ebay_category|gourmet')
    ],
    [
        InlineKeyboardButton(text='📽 Фильмы и сериалы', callback_data='ebay_category|movies'),
        InlineKeyboardButton(text='📷 Фото и видеокамера', callback_data='ebay_category|camera')
    ],
    [
        InlineKeyboardButton(text='🏡 Сад и терраса', callback_data='ebay_category|garden'),
        InlineKeyboardButton(text='📱 Мобильные телефоны', callback_data='ebay_category|phone')
    ],
    [
        InlineKeyboardButton(text='📦 Бытовая техника', callback_data='ebay_category|domestic'),
        InlineKeyboardButton(text='🦮 Зоотовары', callback_data='ebay_category|zoo')
    ],
    [
        InlineKeyboardButton(text='🛠 DIY и ремонт', callback_data='ebay_category|diy'),
        InlineKeyboardButton(text='🔑 Недвижимость', callback_data='ebay_category|property')
    ],
    [
        InlineKeyboardButton(text='👔 Одежда и аксессуары', callback_data='ebay_category|clothes'),
        InlineKeyboardButton(text='🛋 Мебель и гостиная', callback_data='ebay_category|furniture')
    ],
    [
        InlineKeyboardButton(text='🧩 Моделирование', callback_data='ebay_category|modelling'),
        InlineKeyboardButton(text='🪙 Монеты', callback_data='ebay_category|coins')
    ],
    [
        InlineKeyboardButton(text='🎵 Музыка', callback_data='ebay_category|music'),
        InlineKeyboardButton(text='🎻 Музыкальные инструменты', callback_data='ebay_category|music_instruments')
    ],
    [
        InlineKeyboardButton(text='🎮 ПК и видеоигры', callback_data='ebay_category|video_games'),
        InlineKeyboardButton(text='🏕 Путешествия', callback_data='ebay_category|travel')
    ],
    [
        InlineKeyboardButton(text='🏅 Коллекционирование', callback_data='ebay_category|collecting'),
        InlineKeyboardButton(text='🧸 Игрушки', callback_data='ebay_category|toys')
    ],
    [
        InlineKeyboardButton(text='🏌🏻‍♂️ Спорт', callback_data='ebay_category|sport'),
        InlineKeyboardButton(text='🎟 Билеты', callback_data='ebay_category|tickets')
    ],
    [
        InlineKeyboardButton(text='📺 ТВ, видео и аудио', callback_data='ebay_category|tv'),
        InlineKeyboardButton(text='💍 Часы и ювелирные изделия', callback_data='ebay_category|jewelry')
    ],
    [
        InlineKeyboardButton(text='🤿 Разное', callback_data='ebay_category|various'),
        InlineKeyboardButton(text='♾ Все категории сразу', callback_data='ebay_category|all')
    ]
]

ebay_categories = InlineKeyboardMarkup(row_width=3, inline_keyboard=ebay_categories_kb)


async def user_control_keyboard(user_id):
    status = await db.get_user_status(user_id)

    user_control_kb = []


    if status == "active":
        user_control_kb.append([InlineKeyboardButton(text='Выдать подписку', callback_data='give_subscription')])
        user_control_kb.append([InlineKeyboardButton(text='Заблокировать', callback_data='block_user')])
    elif status == "blocked":
        user_control_kb.append([InlineKeyboardButton(text='Выдать подписку', callback_data='give_subscription')])
        user_control_kb.append([InlineKeyboardButton(text='Разблокировать', callback_data='unblock_user')])



    user_control = InlineKeyboardMarkup(row_width=2, inline_keyboard=user_control_kb)

    return user_control


def get_crypto_bot_currencies():
    currencies = ['USDT', 'BUSD', 'USDC', 'BTC', 'ETH', 'TON']
    crypto_bot_currencies_kb = []
    # Размещаем первые 6 значений в 3 ряда
    for i in range(0, len(currencies), 3):

        row_buttons = [InlineKeyboardButton(text=currency, callback_data=f'crypto_bot_currency|{currency}') for currency
                       in currencies[i:i + 3]]
        crypto_bot_currencies_kb.append(row_buttons)
        for currency in currencies[i:i +3]:
            print(f'crypto_bot_currency|{currency}')
    bnb = 'BNB'
    # Проверяем, есть ли дополнительные элементы
    crypto_bot_currencies_kb.append([InlineKeyboardButton(text=bnb, callback_data=f'crypto_bot_currency|{bnb}')])

    # Добавляем кнопку "Отменить действие" в отдельный ряд
    crypto_bot_currencies_kb.append([InlineKeyboardButton(text='❌ Отменить действие', callback_data='cancel')])

    crypto_bot_currencies = InlineKeyboardMarkup(inline_keyboard=crypto_bot_currencies_kb)

    return crypto_bot_currencies


def check_crypto_bot_kb(url: str, invoice_hash: int):
    crypto_bot_status_kb = [
        [InlineKeyboardButton(text='🔗 Оплатить', url=url)],
        [InlineKeyboardButton(text='♻️ Проверить оплату', callback_data=f'check_crypto_bot|{invoice_hash}')]
    ]

    crypto_bot_status = InlineKeyboardMarkup(row_width=1, inline_keyboard=crypto_bot_status_kb)

    return crypto_bot_status


async def get_settings_kb(user_id):
    settings = await db.check_user_settings_kb(user_id)
    settings_kb = []

    first_key_skipped = False
    for column, value in settings.items():
        if not first_key_skipped:
            first_key_skipped = True
            continue

        if column == "item_name":
            column_kb = "Название товара"
        if column == "item_price":
            column_kb = "Цена товара"
        if column == "item_seller":
            column_kb = "Продавец"
        if column == "item_location":
            column_kb = "Расположение товара"
        if column == "item_description":
            column_kb = "Описание товара"
        if column == "item_picture":
            column_kb = "Фото товара"
        if column == "item_publish_date":
            column_kb = "Дата публикации"
        if column == "item_views":
            column_kb = "Показы товара"
        if column == "seller_registration_date":
            column_kb = "Дата регистрации продавца"
        if column == "seller_items_number":
            column_kb = "Кол-во товаров продавца"
        if column == "item_extra_info":
            column_kb = "Дополнительная информация"
        if column == "output_files":
            column_kb = "Вывод в файле"

        if value == 1:
            settings_kb.append([InlineKeyboardButton(text=f'{column_kb} ✅', callback_data=f'{column}_on')])
        elif value == 0:
            settings_kb.append([InlineKeyboardButton(text=f'{column_kb} ❌', callback_data=f'{column}_off')])
        else:
            pass

    settings_keyboard = InlineKeyboardMarkup(row_width=1, inline_keyboard=settings_kb)

    return settings_keyboard




async def get_subscription_kb():
    lengths = await db.get_subscription_time()
    prices = await db.get_subscriptions_price()
    subscribe_kb = []

    for price, length in zip(prices, lengths):
        subscribe_kb.append([InlineKeyboardButton(text=f'{length} [{price}$]', callback_data=f'{length}_sub')])

    subscription = InlineKeyboardMarkup(row_width=1, inline_keyboard=subscribe_kb)

    return subscription


async def get_subscription_kb_for_user():
    lengths = await db.get_subscription_time()
    prices = await db.get_subscriptions_price()
    subscribe_kb = []

    for price, length in zip(prices, lengths):
        subscribe_kb.append([InlineKeyboardButton(text=f'{length} [{price}$]', callback_data=f'sub_to_user|{length}')])

    subscription_to_user = InlineKeyboardMarkup(row_width=1, inline_keyboard=subscribe_kb)

    return subscription_to_user


async def get_subscription_kb_edit():
    lengths = await db.get_subscription_time()
    prices = await db.get_subscriptions_price()
    subscribe_kb_edit = []

    for price, length in zip(prices, lengths):
        subscribe_kb_edit.append([InlineKeyboardButton(text=f'{length} [{price}$]', callback_data=f'{length}_sub_edit')])

    subscription_edit = InlineKeyboardMarkup(row_width=1, inline_keyboard=subscribe_kb_edit)

    return subscription_edit


async def get_klein_presets_kb(user_id):
    presets = await db.get_klein_preset(user_id)



    klein_parser_settings = [
        [
         InlineKeyboardButton(text="Парсинг по нескольким ссылкам", callback_data="klein_links_search")
        ],
        [InlineKeyboardButton(text="Парсинг по ссылке", callback_data='klein_link_search'),
         InlineKeyboardButton(text="Парсинг с фильтрами", callback_data='klein_filters_search')]
    ]
    if presets:
        for preset in presets:
            callback_data = f'klein_preset|{preset[1]}'
            button = InlineKeyboardButton(text=preset[1], callback_data=callback_data)
            klein_parser_settings.append([button])


    klein_parser = InlineKeyboardMarkup(row_width=2, inline_keyboard=klein_parser_settings)

    return klein_parser




depop_au_kb_list = [
    [InlineKeyboardButton(text='Пойск по запросу', callback_data="depop_au_search"),
     InlineKeyboardButton(text='Максимальная цена', callback_data='depop_au_max_price'),
     InlineKeyboardButton(text='Минимальная цена', callback_data='depop_au_min_price'),
     InlineKeyboardButton(text='Сортировка', callback_data='depop_au_sort'),
     InlineKeyboardButton(text='Начать парсинг', callback_data='depop_au_start')]
]


help_kb = [
    [InlineKeyboardButton(text='❓ FAQ', callback_data='faq'),
     InlineKeyboardButton(text='❗️ У меня проблема/вопрос', callback_data='problem_question')]
]

help = InlineKeyboardMarkup(row_width=1, inline_keyboard=help_kb)

