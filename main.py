import itertools
import logging
import multiprocessing
import os
from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, FSInputFile
from scrapy.utils.project import get_project_settings
from app.keyboards import keyboard as kb
from app.keyboards import klein_keyboard as klein_kb
from dotenv import load_dotenv
from app import database as db
from services import parser_output as parse_out
from services import settings_output as settings_out
from states import Balance
from states import subscribe
from states import depop_au_states
from states import ebay_states
from states import users
from states import message
from states import klein_states, klein_states_url, klein_preset_states, klein_links_states
from app.time_functions import time_sub_day, format_timedelta
from app import cryptobot_pay as cp
import time
import asyncio
from scrapy.crawler import CrawlerProcess
from myscrapyproject.depop_au_spider.depop_au_spider.spiders.depop_au import DepopAuSpider
from scrapy.utils.log import configure_logging
from services import ebay
from services.ebay_folder import ebay_de_output
from services.kleinanzeigen import klein
from services.kleinanzeigen import klein_parser_output
from aiocryptopay import AioCryptoPay

form_router = Router()
storage = MemoryStorage()
load_dotenv()
logging.basicConfig(filename="bot.log", level=logging.INFO)
bot: Bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher()


def run_spider(search, priceMax, priceMin, sort, quantity, country):
    configure_logging()
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl(DepopAuSpider, search=search, priceMax=priceMax, priceMin=priceMin, sort=sort, quantity=quantity,
                  country=country)
    process.start()


# Функция, которая будет вызываться в вашем коде для запуска парсера
def run_dep_au_spider(search, priceMax, priceMin, sort, quantity, country):
    # Создаем новый процесс и передаем ему функцию для выполнения
    parser_process = multiprocessing.Process(target=run_spider,
                                             args=(search, priceMax, priceMin, sort, quantity, country))
    # Запускаем процесс
    parser_process.start()
    # Ожидаем завершения процесса (не блокирует основной процесс)
    parser_process.join()
    return "Процесс завершен"


async def on_startup():
    bot_info = await bot.get_me()
    print(f'Бот успешно запущен: {bot_info.username}')
    await db.db_start()


def shutdown(signal, loop):
    print("Программа завершает работу...")
    loop.stop()


@dp.message(F.text == '/start')
async def cmd_start(message: Message):
    await db.cmd_start_db(message.from_user.id)
    await db.cmd_start_user_settings(message.from_user.id)
    ADMIN_ID = os.getenv("ADMIN_ID")
    ADMIN_ID_LIST = [int(admin_id) for admin_id in ADMIN_ID.split(",")]
    status = await db.get_user_status(message.from_user.id)
    if status == "blocked":
        await message.answer('Вы заблокированы!')
    else:
        await message.answer(f'{message.from_user.first_name}, Добро пожаловать!\n\n'
                             f'Вам был выдан приветсвенный баланс 2$\n\n'
                             f'<b>Основные команды бота:</b>\n'
                             f'/start запуск бота,\n'
                             f'/menu запуск меню\n'
                             f'/id получение своего id', reply_markup=kb.main, parse_mode='HTML')
        if message.from_user.id in ADMIN_ID_LIST:
            await message.answer(f'Вы авторизировались как администратор!', reply_markup=kb.main_admin)


@dp.message(F.text == '/id')
async def cmd_id(message: Message):
    status = await db.get_user_status(message.from_user.id)
    if status == "blocked":
        await message.answer('Вы заблокированы!')
    else:
        await message.answer(f'Ваш ID:{message.from_user.id}')


@dp.message(F.text == '/menu')
async def cmd_menu(message: Message):
    status = await db.get_user_status(message.from_user.id)
    if status == "blocked":
        await message.answer('Вы заблокированы!')
    else:
        await message.answer(f'Меню', reply_markup=kb.main)
        ADMIN_ID = os.getenv("ADMIN_ID")
        ADMIN_ID_LIST = [int(admin_id) for admin_id in ADMIN_ID.split(",")]
        if message.from_user.id in ADMIN_ID_LIST:
            await message.answer(f'Вы авторизировались как администратор!', reply_markup=kb.main_admin)


@dp.message(F.text == '🔎 Поиск объявлений' or F.text == 'Поиск объявлений')
async def search(message: Message):
    status = await db.get_user_status(message.from_user.id)
    if status == "blocked":
        await message.answer('Вы заблокированы!')
    else:
        await message.answer('Поиск объявлений ниже:', reply_markup=kb.search_list)


@dp.message(F.text == '💼 Профиль' or F.text == 'Профиль')
async def search(message: Message):
    user_sub = await db.get_time_sub(message.from_user.id)
    if user_sub == 0:
        user_sub = "Нет"
    else:
        user_sub = format_timedelta(time_sub_day(user_sub))
    user_bal = await db.get_balance(message.from_user.id)
    if user_bal == 0:
        user_bal = "0"
    else:
        user_bal = str(user_bal)
    status = await db.get_user_status(message.from_user.id)
    if status == "blocked":
        await message.answer('Вы заблокированы!')
    else:
        await message.answer(
            f'💼 Профиль 💼 \n\n👤 Ваш никнейм: {message.from_user.full_name}\n\n💰 Ваш текущий баланс: — ' + user_bal + ' $' + '\n\n🚀 Активные подписки: ' + user_sub,
            reply_markup=kb.profile, parse_mode="HTML")


@dp.message(F.text == '⚙️ Настройки' or F.text == 'Настройки')
async def search(message: Message):
    status = await db.get_user_status(message.from_user.id)
    if status == "blocked":
        await message.answer('Вы заблокированы!')
    else:
        await message.answer(
            '⚙️ Настройки\n — Нажмите на нужный пункт, чтобы активировать или де-актировать его работу',
            reply_markup=kb.settings)


@dp.message(F.text == 'ℹ️ Помощь' or F.text == 'Помощь')
async def search(message: Message):
    status = await db.get_user_status(message.from_user.id)
    if status == "blocked":
        await message.answer('Вы заблокированы!')
    else:
        await message.answer('Помощь:', reply_markup=kb.help)


@dp.message(F.text == '💻 Админ-Панель')
async def search(message: Message):
    ADMIN_ID = os.getenv("ADMIN_ID")
    ADMIN_ID_LIST = [int(admin_id) for admin_id in ADMIN_ID.split(",")]
    if message.from_user.id in ADMIN_ID_LIST:
        await message.answer(f'Вы вошли в админ-панель', reply_markup=kb.admin_panel)
    else:
        await message.reply("Я тебя не понимаю")


@dp.message(F.text == 'Редактирование подписок')
async def search(message: Message):
    ADMIN_ID = os.getenv("ADMIN_ID")
    ADMIN_ID_LIST = [int(admin_id) for admin_id in ADMIN_ID.split(",")]
    if message.from_user.id in ADMIN_ID_LIST:
        subscription_kb_edit = await kb.get_subscription_kb_edit()
        await message.answer(f'Выберите пункт, который вы хотите отредактировать', reply_markup=subscription_kb_edit)
    else:
        await message.reply("Я тебя не понимаю")


@dp.message(F.text == 'Выслать логи бота')
async def send_logs(message: Message):
    ADMIN_ID = os.getenv("ADMIN_ID")
    ADMIN_ID_LIST = [int(admin_id) for admin_id in ADMIN_ID.split(",")]
    if message.from_user.id in ADMIN_ID_LIST:
        if os.path.exists('bot.log'):
            try:
                log_file = FSInputFile(path='bot.log', filename='bot.log')
                await bot.send_document(message.from_user.id, document=log_file)
            except Exception as e:
                logging.error(f'Ошибка при отправке лог-файла: {e}')
        else:
            # Если файла логов нет, отправляем сообщение об ошибке
            await message.reply('Извините, лог-файл не найден.')


@dp.message(F.text == 'Сделать рассылку')
async def spam_to_bot(message1: Message, state: message.Message.message):
    ADMIN_ID = os.getenv("ADMIN_ID")
    ADMIN_ID_LIST = [int(admin_id) for admin_id in ADMIN_ID.split(",")]
    if message1.from_user.id in ADMIN_ID_LIST:
        await bot.send_message(message1.from_user.id,
                               text="<b>Рассылка всем пользователям бота</b>\n\nПожалуйста, введите сообщение которое вы хотите отправить",
                               parse_mode='HTML')
        await state.set_state(message.Message.message)


@dp.message(StateFilter(message.Message.message))
async def send_message_to_users(message1: Message, state: message.Message.message):
    text_message = message1.text
    users = await db.select_all_users()
    if users:
        for user in users:
            user_id = user[0]
            try:
                await bot.send_message(user_id, text=text_message)
            except Exception as e:
                print(f"Не удалось отправить сообщение пользователю {user_id}: {str(e)}")
        await state.clear()
    else:
        print("Нет пользователей для отправки сообщения.")


@dp.callback_query(lambda callback_query: callback_query.data == 'faq')
async def faq(call: types.CallbackQuery):
    if call.data == 'faq':
        text_message = "<b>Часто задаваемые вопросы:</b>\n\n\n <b>❓Зачем нужен парсер? Что такое парсер?</b>\n❗️" \
                       "Парсер это программа для автоматического и быстрого поиска информации на торговых площадках." \
                       " Парсер предназначен для максимально быстрой и удобной фильтрации информации.\n\n\n" \
                       "<b>❓Как начать пользоваться парсером?</b>\n" \
                       "❗️Для использования парсера Вам понадобится купить подписку на интересующую Вас площадку, после чего Вы можете настроить парсер под себя.\n\n\n" \
                       "<b>❓Как пополнить баланс?</b>\n" \
                       "❗️Для пополнения баланса перейдите в «💼 Профиль» - «💰 Пополнение баланса», после чего выберите удобный способ пополнения.\n\n\n" \
                       "<b>❓Почему мне выдало мало объявлений?</b>\n" \
                       "❗️Выдача объявлений зависит от количества объявлений на сайте и от Ваших фильтров/пресетов," \
                       "чем менее требовательны Ваши пресеты - тем больше объявлений Вам будет выдавать парсер."

        await bot.send_message(call.from_user.id, text=text_message, parse_mode='HTML')


@dp.callback_query(lambda callback_query: callback_query.data == 'problem_question')
async def faq(call: types.CallbackQuery):
    if call.data == "problem_question":
        await bot.send_message(call.from_user.id,
                               text="Обратитесь за помощью администратору проекта https://t.me/crystal812")


@dp.message(F.text == 'Управление пользователями')
async def user_control(message: Message, state: users.Users.user_id):
    ADMIN_ID = os.getenv("ADMIN_ID")
    ADMIN_ID_LIST = [int(admin_id) for admin_id in ADMIN_ID.split(",")]
    if message.from_user.id in ADMIN_ID_LIST:
        await bot.send_message(message.from_user.id,
                               text="<b>Управление пользователями бота</b>\n\nПожалуйста введите ID пользователя",
                               parse_mode='HTML')
        await state.set_state(users.Users.user_id)


@dp.message(StateFilter(users.Users.user_id))
async def check_user_id(message: Message, state: users.Users.user_id):
    await message.delete()
    user_id = message.text
    await state.update_data(user_id=user_id)
    user_info = await db.get_user_info(user_id)
    ADMIN_ID = os.getenv("ADMIN_ID")
    ADMIN_ID_LIST = [int(admin_id) for admin_id in ADMIN_ID.split(",")]
    if user_info is not None:
        _, user_id, subscription, balance, _, status = user_info[0]
        user = await bot.get_chat(user_id)
        username = user.username
        if user_id in ADMIN_ID_LIST:
            admin_text = '<b>Администратор</b>'
        else:
            admin_text = ""
        if subscription is not None:
            subscription_text = format_timedelta(time_sub_day(subscription))
        else:
            subscription_text = "Подписка отсутствует"
        if status == "active":
            status = "Активен"
        elif status == "blocked":
            status = "Заблокирован"
        user_kb = await kb.user_control_keyboard(user_id)
        await bot.send_message(message.from_user.id, text=f'<b>Информация о пользователе:</b>\n\n'
                                                          f'{admin_text}\n'
                                                          f'ID: {user_id}\n'
                                                          f'Username: {username}\n'
                                                          f'Подписка: {subscription_text}\n'
                                                          f'Баланс: {balance} $\n'
                                                          f'Статус: {status}', parse_mode='HTML', reply_markup=user_kb)

    else:
        await bot.send_message(message.from_user.id, text='<b>Пожалуйста введите корректное ID пользователя!</b>',
                               parse_mode='HTML')


@dp.callback_query(lambda callback_query: callback_query.data == 'give_subscription')
async def give_subscription(call: types.CallbackQuery):
    sub_keyboard = await kb.get_subscription_kb_for_user()
    await bot.send_message(call.from_user.id, text="Выберите подписку для выдачи пользователю",
                           reply_markup=sub_keyboard)


@dp.callback_query(lambda callback_query: callback_query.data == 'block_user')
async def block_user_by_id(call: types.CallbackQuery, state: users.Users.user_id):
    user_data = await state.get_data()
    user_id = user_data.get('user_id')
    await db.block_user(user_id)
    await bot.send_message(call.from_user.id,
                           text=f"<b>Пользователь с ID: {user_id} был успешно заблокирован</b>\n\n Для разблокировки, заново войдите в меню управления пользователями",
                           parse_mode='HTML')
    await state.clear()


@dp.callback_query(lambda callback_query: callback_query.data == 'unblock_user')
async def unblock_user_by_id(call: types.CallbackQuery, state: users.Users.user_id):
    user_data = await state.get_data()
    user_id = user_data.get('user_id')
    await db.unblock_user(user_id)
    await bot.send_message(call.from_user.id,
                           text=f"<b>Пользователь с ID: {user_id} был успешно разблокирован</b>\n\n Для блокировки, заново войдите в меню управления пользователями",
                           parse_mode='HTML')
    await state.clear()


@dp.callback_query(lambda callback_query: callback_query.data.startswith('sub_to_user|'))
async def give_subscription_to_user(call: types.CallbackQuery, state: users.Users.user_id):
    lengths = await db.get_subscription_time()
    user_data = await state.get_data()
    user_id = user_data.get('user_id')
    if lengths:
        length1 = lengths[0]
        length2 = lengths[1]
        length3 = lengths[2]
        length4 = lengths[3]
        if call.data == f'sub_to_user|{length1}':
            subscription = await db.get_time_sub(user_id)
            if subscription > int(time.time()):
                await bot.send_message(call.from_user.id, text='У этого пользователя уже есть подписка')
                await state.clear()
            else:
                await db.give_time_sub_1day(user_id)
                await bot.send_message(call.from_user.id,
                                       text=f'Подписка на один день для пользователя <b>{user_id}</b> была успешно оформлена!',
                                       parse_mode='HTML')
                await bot.send_message(user_id, text='Вам была выдана подписка на 1 день!\n\n'
                                                     'С уважением, Администрация!')
                await state.clear()
        elif call.data == f'sub_to_user|{length2}':
            subscription = await db.get_time_sub(user_id)
            if subscription > int(time.time()):
                await bot.send_message(call.from_user.id, text='У этого пользователя уже есть подписка')
                await state.clear()
            else:
                await db.give_time_sub_3days(user_id)
                await bot.send_message(call.from_user.id,
                                       text=f'Подписка на 3 дня для пользователя <b>{user_id}</b> была успешно оформлена!',
                                       parse_mode='HTML')
                await bot.send_message(user_id, text='Вам была выдана подписка на 3 дня!\n\n'
                                                     'С уважением, Администрация!')
                await state.clear()
        elif call.data == f'sub_to_user|{length3}':
            subscription = await db.get_time_sub(user_id)
            if subscription > int(time.time()):
                await bot.send_message(call.from_user.id, text='У этого пользователя уже есть подписка')
                await state.clear()
            else:
                await db.give_time_sub_1week(user_id)
                await bot.send_message(call.from_user.id,
                                       text=f'Подписка на 1 неделю для пользователя <b>{user_id}</b> была успешно оформлена!',
                                       parse_mode='HTML')
                await bot.send_message(user_id, text='Вам была выдана подписка на 1 неделю!\n\n'
                                                     'С уважением, Администрация!')
                await state.clear()
        elif call.data == f'sub_to_user|{length4}':
            subscription = await db.get_time_sub(user_id)
            if subscription > int(time.time()):
                await bot.send_message(call.from_user.id, text='У этого пользователя уже есть подписка')
                await state.clear()
            else:
                await db.give_time_sub_1month(user_id)
                await bot.send_message(call.from_user.id,
                                       text=f'Подписка на 1 месяц для пользователя <b>{user_id}</b> была успешно оформлена!',
                                       parse_mode='HTML')
                await bot.send_message(user_id, text='Вам была выдана подписка на 1 месяц!\n\n'
                                                     'С уважением, Администрация!')
                await state.clear()


@dp.message(StateFilter(None))
async def echo(message: Message):
    # Получаем информацию о чате
    chat_info = await bot.get_chat(chat_id=message.chat.id)

    # Проверяем, существует ли закрепленное сообщение и его текст
    if chat_info.pinned_message and chat_info.pinned_message.text.startswith("Отчет о парсинге") or chat_info.pinned_message.text.startswith("Парсинг начал работу"):
        return  # Ничего не делаем, так как уже есть закрепленное сообщение
    else:
        await message.reply("Я тебя не понимаю, бот находится в разработке")


@dp.callback_query(lambda callback_query: callback_query.data in ['DEPOP', 'EBAY', 'KLEINANZEIGEN', 'ETSY'])
async def handle_service_queries(callback_query: types.CallbackQuery):
    if callback_query.data == 'DEPOP':
        await bot.send_message(callback_query.from_user.id, text='DEPOP Сервисы', reply_markup=kb.depop_list)
    elif callback_query.data == 'EBAY':
        await bot.send_message(callback_query.from_user.id, text='EBAY Сервисы', reply_markup=kb.ebay_list)
    elif callback_query.data == 'KLEINANZEIGEN':
        await bot.send_message(callback_query.from_user.id, text='KLEINANZEIGEN Сервисы', reply_markup=kb.klein_list)
    elif callback_query.data == "ETSY":
        await bot.send_message(callback_query.from_user.id, text='ETSY Сервисы', reply_markup=kb.etsy_list)



@dp.callback_query(lambda callback_query: callback_query.data == "EBAY_DE")
async def handler_ebay(callback_query: types.CallbackQuery, state: ebay_states.Ebay.search):
    if callback_query.data == 'EBAY_DE':
        user_subscription = await db.get_time_sub(callback_query.from_user.id)
        if user_subscription == 0:
            await bot.send_message(callback_query.from_user.id,
                                   text="Подписка отсутствует, приобретите подписку во вкладе 'Профиль'")
        elif user_subscription < int(time.time()):
            await bot.send_message(callback_query.from_user.id,
                                   text="Подписка истекла, приобретите подписку во вкладе 'Профиль'")
        else:
            await bot.send_message(callback_query.from_user.id,
                                   text="Вы выбрали EBAY Germany 🇩🇪  \nФильтры доступные для настройки: \n\nВыбор категории (по умолчанию 'Все категории'\n\nПоисковый запрос (по умолчанию 'monitor')\n\nМаксимальная цена (по умолчанию равна 500 EURO)\n\nМинимальная цена(по умолчанию равна 50 EURO)\n\nСортировка (по умолчанию Релевантность)\n\nКоличество товаров для вывода(по умолчанию 25)")
            await bot.send_message(callback_query.from_user.id,
                                   text="<b>Выберите нужную вам категорию</b>, самая последняя кнопка выбирает пойск по всем категориям!",
                                   reply_markup=kb.ebay_categories, parse_mode='HTML')
            await state.set_state(ebay_states.Ebay.search)
            logging.info('Это сообщение будет записано в файл bot.log')


@dp.callback_query(lambda callback_query: callback_query.data.startswith('ebay_category|'))
async def ebay_de_category(call: types.CallbackQuery, state: ebay_states.Ebay.category):
    sacat_dict = {
        'antique': 353,
        'transport': 9800,
        'details': 131090,
        'baby': 2984,
        'craft': 14339,
        'beauty': 26395,
        'stamps': 260,
        'books': 267,
        'office': 9815,
        'business': 12576,
        'computer': 58058,
        'gourmet': 14308,
        'movies': 11232,
        'camera': 625,
        'garden': 159912,
        'phone': 15032,
        'domestic': 20710,
        'zoo': 1281,
        'diy': 3187,
        'property': 10542,
        'clothes': 11450,
        'furniture': 11700,
        'modelling': 2212,
        'coins': 11116,
        'music': 11233,
        'music_instruments': 619,
        'video_games': 1249,
        'travel': 3252,
        'collecting': 1,
        'toys': 220,
        'sport': 888,
        'tickets': 1305,
        'tv': 293,
        'jewelry': 281,
        'various': 99,
        'all': 0
    }
    category = call.data.split('|')[1]
    sacat = sacat_dict.get(category)
    print(sacat)
    await state.update_data(category=sacat)
    await bot.send_message(call.from_user.id,
                           text=f"Категория {category} была выбрана\n\nВведите ваш поисковый запрос для парсинга, если вы хотите оставить запрос по умолчанию, то введите '1'")
    await state.set_state(ebay_states.Ebay.search)


@dp.message(StateFilter(ebay_states.Ebay.search))
async def ebay_de_search(message: Message, state: ebay_states.Ebay.search):
    search_param = message.text
    await state.update_data(search=search_param)
    await bot.send_message(message.from_user.id,
                           text="Введите параметр максимальной цены для парсинга, чтобы оставить по умолчанию введите 'def'")
    await state.set_state(ebay_states.Ebay.priceMax)


@dp.message(StateFilter(ebay_states.Ebay.priceMax))
async def ebay_de_price_max(message: Message, state: ebay_states.Ebay.priceMax):
    try:
        priceMax = message.text
        await state.update_data(priceMax=priceMax)
        await bot.send_message(message.from_user.id,
                               text="Введите параметр минимальной цены для парсинга, чтобы оставить по умолчанию введите 'def'")
        await state.set_state(ebay_states.Ebay.priceMin)
    except ValueError:
        await bot.send_message(message.from_user.id, text="Пожалуйста, введите корректное число для 'priceMax'.")


@dp.message(StateFilter(ebay_states.Ebay.priceMin))
async def ebay_de_price_min(message: Message, state: ebay_states.Ebay.priceMin):
    try:
        priceMin = message.text
        await state.update_data(priceMin=priceMin)
        await bot.send_message(message.from_user.id,
                               text="Введите параметр сортировки для парсинга (например, 'релевантность', 'по возрастанию', 'по убыванию', 'скоро закончится', 'ближайшие'):")
        await state.set_state(ebay_states.Ebay.sort)
    except ValueError:
        await bot.send_message(message.from_user.id, text="Пожалуйста, введите корректное число для 'priceMax'.")


@dp.message(StateFilter(ebay_states.Ebay.sort))
async def ebay_de_sort(message: Message, state: ebay_states.Ebay.sort):
    sort = message.text
    await state.update_data(sort=sort)
    await bot.send_message(message.from_user.id, text="Введите количество товаров для вывода (максимум 80)")
    await state.set_state(ebay_states.Ebay.quantity)


@dp.message(StateFilter(ebay_states.Ebay.quantity))
async def ebay_de_quantity(message: Message, state: ebay_states.Ebay.quantity):
    quantity = message.text
    await state.update_data(quantity=quantity)
    user_data = await state.get_data()
    search = user_data.get('search')
    search = search.replace(" ", "+")
    priceMax = user_data.get('priceMax')
    priceMin = user_data.get('priceMin')
    sort = user_data.get('sort')
    quantity = user_data.get('quantity')
    sacat = user_data.get("category")
    if search == "1" or search is None or search.isdigit():
        search = "monitor"
    if priceMax == "def" or priceMax is None or not priceMax.isdigit():
        priceMax = 500
    if priceMin == "def" or priceMin is None or not priceMax.isdigit():
        priceMin = 50
    if quantity is None or int(quantity) > 80 or int(quantity) < 0 or not quantity.isdigit():
        quantity = 25

    if sort is None or sort == "релевантность" or sort == "Релевантность":
        sort = "12"
    elif sort == "по возрастанию" or sort == "По возрастанию":
        sort = "3"
    elif sort == "по убыванию" or sort == "По убыванию":
        sort = "2"
    elif sort == "скоро закончится" or sort == "Скоро закончится":
        sort = "1"
    elif sort == "ближайшие" or sort == "Ближайшие":
        sort = "7"
    else:
        sort = "12"

    await bot.send_message(message.from_user.id, text='Парсинг запущен... Ожидайте')
    process = await ebay.ebay_de_parser(search, sacat, priceMin, priceMax, sort, quantity)
    if process == "Finished":
        await bot.send_message(message.from_user.id, text='Парсинг завершен!')
        output = await ebay_de_output.output_ebay_de(message.from_user.id)
        for item in output:
            await bot.send_message(message.from_user.id, item, parse_mode="HTML")
        parser_output_file = FSInputFile(path='services/ebay_folder/ebay_de_output.json',
                                         filename='ebay_de_output.json')
        await bot.send_document(message.from_user.id, document=parser_output_file)
        await state.clear()
        logging.info('Это сообщение будет записано в файл bot.log')
    else:
        await bot.send_message(message.from_user.id, text='Ошибка, обратитесь в поддержку во вкладке "Помощь"')
    await state.clear()


@dp.callback_query(lambda callback_query: callback_query.data in ['DEPOP_AU', 'DEPOP_DE', 'DEPOP_FR', 'DEPOP_GB', 'DEPOP_IT',
                                                   'DEPOP_US'])
async def handler_depop(callback_query: types.CallbackQuery, state: depop_au_states.DepopAu.search):
    if callback_query.data == 'DEPOP_AU':
        user_subscription = await db.get_time_sub(callback_query.from_user.id)
        if user_subscription == 0:
            await bot.send_message(callback_query.from_user.id,
                                   text="Подписка отсутствует, приобретите подписку во вкладе 'Профиль'")
        elif user_subscription < int(time.time()):
            await bot.send_message(callback_query.from_user.id,
                                   text="Подписка истекла, приобретите подписку во вкладе 'Профиль'")
        else:
            await bot.send_message(callback_query.from_user.id,
                                   text="Вы выбрали DEPOP Australia 🇦🇺 \nФильтры доступные для настройки: \n\nПоисковый запрос (по умолчанию streetwear)\n\nМаксимальная цена (по умолчанию равна 500 AUD)\n\nМинимальная цена(по умолчанию равна 50 AUD)\n\nСортировка (по умолчанию Релевантность)\n\nКоличество товаров для вывода(по умолчанию 25)")
            await bot.send_message(callback_query.from_user.id,
                                   text="Введите ваш поисковый запрос для парсинга, если вы хотите оставить запрос по умолчанию, то введите '1'")
            await state.update_data(country="au")
            await state.set_state(depop_au_states.DepopAu.search)
            logging.info('Это сообщение будет записано в файл bot.log')
    elif callback_query.data == "DEPOP_DE":
        user_subscription = await db.get_time_sub(callback_query.from_user.id)
        if user_subscription == 0:
            await bot.send_message(callback_query.from_user.id,
                                   text="Подписка отсутствует, приобретите подписку во вкладе 'Профиль'")
        elif user_subscription < int(time.time()):
            await bot.send_message(callback_query.from_user.id,
                                   text="Подписка истекла, приобретите подписку во вкладе 'Профиль'")
        else:
            await bot.send_message(callback_query.from_user.id,
                                   text="Вы выбрали DEPOP Germany 🇩🇪 \nФильтры доступные для настройки: \n\nПоисковый запрос (по умолчанию streetwear)\n\nМаксимальная цена (по умолчанию равна 500 EURO)\n\nМинимальная цена(по умолчанию равна 50 EURO)\n\nСортировка (по умолчанию Релевантность)\n\nКоличество товаров для вывода(по умолчанию 25)")
            await bot.send_message(callback_query.from_user.id,
                                   text="Введите ваш поисковый запрос для парсинга, если вы хотите оставить запрос по умолчанию, то введите '1'")
            await state.update_data(country="de")
            await state.set_state(depop_au_states.DepopAu.search)
            logging.info('Это сообщение будет записано в файл bot.log')
    elif callback_query.data == "DEPOP_FR":
        user_subscription = await db.get_time_sub(callback_query.from_user.id)
        if user_subscription == 0:
            await bot.send_message(callback_query.from_user.id,
                                   text="Подписка отсутствует, приобретите подписку во вкладе 'Профиль'")
        elif user_subscription < int(time.time()):
            await bot.send_message(callback_query.from_user.id,
                                   text="Подписка истекла, приобретите подписку во вкладе 'Профиль'")
        else:
            await bot.send_message(callback_query.from_user.id,
                                   text="Вы выбрали DEPOP France 🇫🇷 \nФильтры доступные для настройки: \n\nПоисковый запрос (по умолчанию streetwear)\n\nМаксимальная цена (по умолчанию равна 500 EURO)\n\nМинимальная цена(по умолчанию равна 50 EURO)\n\nСортировка (по умолчанию Релевантность)\n\nКоличество товаров для вывода(по умолчанию 25)")
            await bot.send_message(callback_query.from_user.id,
                                   text="Введите ваш поисковый запрос для парсинга, если вы хотите оставить запрос по умолчанию, то введите '1'")
            await state.update_data(country="fr")
            await state.set_state(depop_au_states.DepopAu.search)
            logging.info('Это сообщение будет записано в файл bot.log')
    elif callback_query.data == "DEPOP_GB":
        user_subscription = await db.get_time_sub(callback_query.from_user.id)
        if user_subscription == 0:
            await bot.send_message(callback_query.from_user.id,
                                   text="Подписка отсутствует, приобретите подписку во вкладе 'Профиль'")
        elif user_subscription < int(time.time()):
            await bot.send_message(callback_query.from_user.id,
                                   text="Подписка истекла, приобретите подписку во вкладе 'Профиль'")
        else:
            await bot.send_message(callback_query.from_user.id,
                                   text="Вы выбрали DEPOP United Kingdom 🇬🇧 \nФильтры доступные для настройки: \n\nПоисковый запрос (по умолчанию streetwear)\n\nМаксимальная цена (по умолчанию равна 500 GBP)\n\nМинимальная цена(по умолчанию равна 50 GBP)\n\nСортировка (по умолчанию Релевантность)\n\nКоличество товаров для вывода(по умолчанию 25)")
            await bot.send_message(callback_query.from_user.id,
                                   text="Введите ваш поисковый запрос для парсинга, если вы хотите оставить запрос по умолчанию, то введите '1'")
            await state.update_data(country="gb")
            await state.set_state(depop_au_states.DepopAu.search)
            logging.info('Это сообщение будет записано в файл bot.log')
    elif callback_query.data == "DEPOP_IT":
        user_subscription = await db.get_time_sub(callback_query.from_user.id)
        if user_subscription == 0:
            await bot.send_message(callback_query.from_user.id,
                                   text="Подписка отсутствует, приобретите подписку во вкладе 'Профиль'")
        elif user_subscription < int(time.time()):
            await bot.send_message(callback_query.from_user.id,
                                   text="Подписка истекла, приобретите подписку во вкладе 'Профиль'")
        else:
            await bot.send_message(callback_query.from_user.id,
                                   text="Вы выбрали DEPOP Italy 🇮🇹 \nФильтры доступные для настройки: \n\nПоисковый запрос (по умолчанию streetwear)\n\nМаксимальная цена (по умолчанию равна 500 EURO)\n\nМинимальная цена(по умолчанию равна 50 EURO)\n\nСортировка (по умолчанию Релевантность)\n\nКоличество товаров для вывода(по умолчанию 25)")
            await bot.send_message(callback_query.from_user.id,
                                   text="Введите ваш поисковый запрос для парсинга, если вы хотите оставить запрос по умолчанию, то введите '1'")
            await state.update_data(country="it")
            await state.set_state(depop_au_states.DepopAu.search)
            logging.info('Это сообщение будет записано в файл bot.log')
    elif callback_query.data == "DEPOP_US":
        user_subscription = await db.get_time_sub(callback_query.from_user.id)
        if user_subscription == 0:
            await bot.send_message(callback_query.from_user.id,
                                   text="Подписка отсутствует, приобретите подписку во вкладе 'Профиль'")
        elif user_subscription < int(time.time()):
            await bot.send_message(callback_query.from_user.id,
                                   text="Подписка истекла, приобретите подписку во вкладе 'Профиль'")
        else:
            await bot.send_message(callback_query.from_user.id,
                                   text="Вы выбрали DEPOP United States 🇺🇸 \nФильтры доступные для настройки: \n\nПоисковый запрос (по умолчанию streetwear)\n\nМаксимальная цена (по умолчанию равна 500 USD)\n\nМинимальная цена(по умолчанию равна 50 USD)\n\nСортировка (по умолчанию Релевантность)\n\nКоличество товаров для вывода(по умолчанию 25)")
            await bot.send_message(callback_query.from_user.id,
                                   text="Введите ваш поисковый запрос для парсинга, если вы хотите оставить запрос по умолчанию, то введите '1'")
            await state.update_data(country="us")
            await state.set_state(depop_au_states.DepopAu.search)
            logging.info('Это сообщение будет записано в файл bot.log')


@dp.message(StateFilter(depop_au_states.DepopAu.search))
async def depop_search(message: Message, state: depop_au_states.DepopAu.search):
    search_param = message.text
    await state.update_data(search=search_param)
    await bot.send_message(message.from_user.id, text="Введите параметр максимальной цены для парсинга:")
    await state.set_state(depop_au_states.DepopAu.priceMax)


@dp.message(StateFilter(depop_au_states.DepopAu.priceMax))
async def depop_price_max(message: types.Message, state: depop_au_states.DepopAu.priceMax):
    try:
        priceMax = message.text
        await state.update_data(priceMax=priceMax)
        await bot.send_message(message.from_user.id, text="Введите параметр минимальной цены для парсинга:")
        await state.set_state(depop_au_states.DepopAu.priceMin)
    except ValueError:
        await bot.send_message(message.from_user.id, text="Пожалуйста, введите корректное число для 'priceMax'.")


@dp.message(StateFilter(depop_au_states.DepopAu.priceMin))
async def depop_price_min(message: types.Message, state: depop_au_states.DepopAu.priceMin):
    try:
        priceMin = message.text
        await state.update_data(priceMin=priceMin)
        await bot.send_message(message.from_user.id,
                               text="Введите параметр сортировки для парсинга (например, 'релевантность', 'по возрастанию', 'по убыванию', 'популярные', 'новые'):")
        await state.set_state(depop_au_states.DepopAu.sort)
    except ValueError:
        await bot.send_message(message.from_user.id, text="Пожалуйста, введите корректное число для 'priceMin'.")


@dp.message(StateFilter(depop_au_states.DepopAu.sort))
async def depop_sort(message: types.Message, state: depop_au_states.DepopAu.sort):
    sort = message.text
    await state.update_data(sort=sort)
    await bot.send_message(message.from_user.id, text="Введите количество товаров, которое вам нужно(максимально 80)")
    await state.set_state(depop_au_states.DepopAu.quantity)


@dp.message(StateFilter(depop_au_states.DepopAu.quantity))
async def depop_quantity(message: types.Message, state: depop_au_states.DepopAu.quantity):
    quantity = message.text
    await state.update_data(quantity=quantity)

    user_data = await state.get_data()
    search = user_data.get('search')
    priceMax = user_data.get('priceMax')
    priceMin = user_data.get('priceMin')
    sort = user_data.get('sort')
    quantity = user_data.get('quantity')
    country = user_data.get('country')

    if search == "1" or search is None or search.isdigit():
        search = "streetwear"

    if priceMax == "default" or priceMax is None or not priceMax.isdigit():
        priceMax = 500
    if priceMin == "default" or priceMin is None or not priceMax.isdigit():
        priceMin = 50
    if sort is None or sort == "релевантность" or sort == "Релевантность":
        sort = "relevance"
    elif sort == "по возрастанию" or sort == "По возрастанию":
        sort = "priceAscending"
    elif sort == "по убыванию" or sort == "По убыванию":
        sort = "priceDescending"
    elif sort == "популярные" or sort == "Популярные":
        sort = "popular"
    elif sort == "новые" or sort == "Новые":
        sort = "newlyListed"
    if quantity is None or int(quantity) > 80 or int(quantity) < 0 or not quantity.isdigit():
        quantity = 25

    await bot.send_message(message.from_user.id, text='Парсинг запущен... Ожидайте')
    process_depop = run_dep_au_spider(search, priceMax, priceMin, sort, quantity, country)
    if process_depop == "Процесс завершен":
        await bot.send_message(message.from_user.id, text='Парсинг завершен!')
        output = await parse_out.output_depop_au(message.from_user.id)
        for item in output:
            await bot.send_message(message.from_user.id, item, parse_mode="HTML")
        parser_output_file = FSInputFile(path='scraped_data_depop.json', filename='scraped_data_depop.json')
        await bot.send_document(message.from_user.id, document=parser_output_file)
        await state.clear()
        logging.info('Это сообщение будет записано в файл bot.log')
    else:
        await bot.send_message(message.from_user.id, text='Ошибка, обратитесь в поддержку во вкладке "Помощь"')
    await state.clear()


@dp.callback_query(lambda callback_query: callback_query.data == "klein")
async def klein_parser_choice(call: types.CallbackQuery):
    if call.data == "klein":
        await call.message.delete()
        user_subscription = await db.get_time_sub(call.from_user.id)
        if user_subscription == 0:
            await bot.send_message(call.from_user.id,
                                   text="Подписка отсутствует, приобретите подписку во вкладе 'Профиль'")
        elif user_subscription < int(time.time()):
            await bot.send_message(call.from_user.id,
                                   text="Подписка истекла, приобретите подписку во вкладе 'Профиль'")
        else:
            klein_parser_kb = await kb.get_klein_presets_kb(call.from_user.id)
            await bot.send_message(call.from_user.id,
                                   text="Вы выбрали KLEINANZEIGEN 🇩🇪 \n\n<b>Выберите параметр для парсинга</b>",
                                   reply_markup=klein_parser_kb, parse_mode='HTML')


@dp.callback_query(lambda callback_query: callback_query.data in ["klein_links_search", "klein_link_search", "klein_filters_search"])
async def klein_parser_search(call: types.CallbackQuery, state: klein_states_url.KleinUrl.url):
    if call.data == "klein_links_search":
        await call.message.delete()
        await bot.send_message(call.from_user.id, text="<b>Чтобы осуществить пойск по ссылкам вам потребуется:</b>\n\n\n"
                                                       "1. Зайти на сайт сервиса https://www.kleinanzeigen.de/\n"
                                                       "2. Выполнить пойск товаров по вашему запросу\n"
                                                       "3. Выбрать нужные категории и фильтры\n"
                                                       "4. Отправить ссылкы в бота, по ней произведется парсинг\n\n\n"
                                                       "<b>Отправляйте ссылки через пробел или в каждой новой строке</b>",
                               parse_mode='HTML')
        await bot.send_message(call.from_user.id, text="Отправьте ваши ссылки для парсинга")
        await state.set_state(klein_links_states.KleinLinks.links)
    elif call.data == "klein_link_search":
        await call.message.delete()
        await bot.send_message(call.from_user.id, text="<b>Чтобы осуществить пойск по ссылке вам потребуется:</b>\n\n\n"
                                                       "1. Зайти на сайт сервиса https://www.kleinanzeigen.de/\n"
                                                       "2. Выполнить пойск товаров по вашему запросу\n"
                                                       "3. Выбрать нужные категории и фильтры\n"
                                                       "4. Отправить ссылку в бота, по ней произведется парсинг\n",
                               parse_mode='HTML')
        await bot.send_message(call.from_user.id, text="Введите вашу ссылку для парсинга")
        await state.set_state(klein_states_url.KleinUrl.url)
    elif call.data == "klein_filters_search":
        await bot.send_message(call.from_user.id,
                               text="Вы выбрали KLEINANZEIGEN 🇩🇪 \nФильтры доступные для настройки:\n\nВыбор категорий \n\nПоисковый запрос (по умолчанию bycicle)\n\nМаксимальная цена (по умолчанию равна 500 EURO)\n\nМинимальная цена(по умолчанию равна 50 EURO)\n\nСортировка (по умолчанию Релевантность)\n\nКоличество товаров для вывода(по умолчанию 25)",
                               reply_markup=klein_kb.klein_categories)



@dp.message(StateFilter(klein_links_states.KleinLinks.links))
async def klein_parsing_by_links(message: types.Message, state: klein_links_states.KleinLinks.links):
    links = message.text
    link_list = links.splitlines()


    async def start_links_parser(user_id, links):
        try:
            await klein.klein_links_parsing(user_id, links)
            await bot.send_message(message.from_user.id, text="Парсинг был завершен!")
        except Exception as e:
            logging.error(f'Ошибка во время парсинга: {e}')
            await bot.send_message(message.from_user.id,
                                   text="Произошла ошибка во время парсинга. Пожалуйста, попробуйте снова позже.")

    loop.create_task(start_links_parser(message.from_user.id, link_list))

    async def display_klein_status():
        report_message = f"<b>Парсинг начал работу:</b> \n\n\n" \
                         f"Сервис: <b>Kleinanzeigen</b> \n\n" \
                         f"Количество спаршенных данных: 0\n\n" \
                         f"Выберите дальнейшие действия: "

        try:
            await bot.send_message(message.from_user.id, text="Парсинг запущен, ожидайте")
            await message.delete()
            sent_message = await bot.send_message(message.from_user.id,
                                                  text=report_message,
                                                  reply_markup=kb.klein_after_parsing,
                                                  disable_web_page_preview=True,
                                                  parse_mode="HTML")

            await bot.pin_chat_message(chat_id=message.from_user.id,
                                       message_id=sent_message.message_id)
        except Exception as e:
            logging.error(f'Ошибка при обновлении сообщения: {e}')

    asyncio.create_task(display_klein_status())


@dp.callback_query(lambda callback_query: callback_query.data.startswith("klein_preset|"))
async def klein_preset_parsing(call: types.CallbackQuery, state: klein_preset_states.KleinState.name):
    preset_name = call.data.split('|')[1]  # Извлекаем название пресета из callback_data
    print(preset_name)
    presets = await db.get_klein_preset_by_name(call.from_user.id, preset_name)
    for preset in presets:
        if call.data == f"klein_preset|{preset[1]}":
            await bot.send_message(call.from_user.id, text=f"<b>Ваш пресет</b>\n\n"
                                                           f"Название: {preset[1]}\n"
                                                           f"Категория: {preset[2]}\n"
                                                           f"Поисковый запрос: {preset[3]}\n"
                                                           f"Максимальная цена: {preset[4]}\n"
                                                           f"Минимальная цена: {preset[5]}\n"
                                                           f"Сортировка: {preset[6]}", parse_mode="HTML", reply_markup=klein_kb.klein_parse_preset)
            await state.update_data(name=preset_name)



@dp.callback_query(lambda callback_query: callback_query.data in ["klein_preset_parsing", "klein_delete_preset"])
async def klein_preset_parsing_choose(call: types.CallbackQuery, state: klein_preset_states.KleinState.name):
    if call.data == "klein_preset_parsing":
        user_data = await state.get_data()
        preset_name = user_data.get("name")
        await bot.send_message(call.from_user.id, text="Введите количество товаров для вывода")
        await state.set_state(klein_preset_states.KleinState.quantity)
    elif call.data == "klein_delete_preset":
        user_data = await state.get_data()
        preset_name = user_data.get("name")
        await db.delete_klein_preset(call.from_user.id, preset_name)
        await bot.send_message(call.from_user.id, text=f"Ваш пресет '{preset_name}' был успешно удален")
        await state.clear()



@dp.message(StateFilter(klein_preset_states.KleinState.quantity))
async def klein_preset_parsing(message: types.Message, state: klein_preset_states.KleinState.quantity):
    quantity = message.text
    user_data = await state.get_data()
    preset_name = user_data.get("name")
    category = None
    search = None
    priceMax = None
    priceMin = None
    sort = None
    presets = await db.get_klein_preset_by_name(message.from_user.id, preset_name)
    if presets:
        for preset in presets:
            category = preset[2]
            search = preset[3]
            priceMax = preset[4]
            priceMin = preset[5]
            sort = preset[6]
            if sort == "По дате создания":
                sort = ""
            elif sort == "По возрастанию цены":
                sort = "sortierung:preis"

        async def run_klein_parsing(user_id, category, search, priceMax, priceMin, sort, quantity):

            try:
                await klein.klein_parsing_with_filters(user_id, category, search, priceMax, priceMin, sort, quantity)
                await bot.send_message(message.from_user.id, text="Парсинг был завершен!")
            except Exception as e:
                logging.error(f'Ошибка во время парсинга: {e}')
                await bot.send_message(message.from_user.id,
                                       text="Произошла ошибка во время парсинга. Пожалуйста, попробуйте снова позже.")

        loop.create_task(run_klein_parsing(message.from_user.id, category, search, priceMax, priceMin, sort, quantity))

        async def display_klein_status(quantity):
            report_message = f"<b>Парсинг начал работу:</b> \n\n\n" \
                             f"Сервис: <b>Kleinanzeigen</b> \n\n" \
                             f"Количество спаршенных данных: 0\n\n" \
                             f"Количество сообщений для отправки: {quantity}\n\n" \
                             f"Выберите дальнейшие действия: "

            try:
                await bot.send_message(message.from_user.id, text="Парсинг запущен, ожидайте")
                await message.delete()
                sent_message = await bot.send_message(message.from_user.id,
                                                      text=report_message,
                                                      reply_markup=kb.klein_after_parsing,
                                                      disable_web_page_preview=True,
                                                      parse_mode="HTML")

                await bot.pin_chat_message(chat_id=message.from_user.id,
                                           message_id=sent_message.message_id)
            except Exception as e:
                logging.error(f'Ошибка при обновлении сообщения: {e}')

        asyncio.create_task(display_klein_status(quantity))

    else:
        await bot.send_message(message.from_user.id, text="Ваш пресет не был найден, обратитесь в поддержку либо попробуйте еще раз")




@dp.callback_query(lambda callback_query: callback_query.data in ["save_klein_preset", "not_save_klein_preset"])
async def klein_save_preset_choose(call: types.CallbackQuery, state: klein_preset_states.KleinState.name):
    if call.data == "save_klein_preset":
        await call.message.delete()
        await bot.send_message(call.from_user.id, text="Введите название для вашего пресета:")
        await state.set_state(klein_preset_states.KleinState.name)
    elif call.data == "not_save_klein_preset":
        await call.message.delete()



@dp.message(StateFilter(klein_preset_states.KleinState.name))
async def klein_save_preset(message: types.Message, state: klein_states.Klein):
    preset_name = message.text
    user_data = await state.get_data()
    search = user_data.get('search')
    search = search.replace(" ", "-")
    priceMax = user_data.get('priceMax')
    priceMin = user_data.get('priceMin')
    sort = user_data.get('sort')
    quantity = user_data.get('quantity')
    category = user_data.get("category")
    sort_message = None
    if search == "1" or search is None:
        search = "bicycle"
    else:
        search = search.replace(" ", "-")
    if priceMax == "def" or priceMax is None or not priceMax.isdigit():
        priceMax = 500
    if priceMin == "def" or priceMin is None or not priceMax.isdigit():
        priceMin = 50
    if quantity is None or int(quantity) > 100 or int(quantity) < 0 or not quantity.isdigit():
        quantity = 25
    if sort == "по дате создания" or sort == "По дате создания":
        sort = ""
        sort_message = "По дате создания"
    elif sort == "по возрастанию цены" or sort == "По возрастанию цены":
        sort = "sortierung:preis"
        sort_message = "По возрастанию цены"

    await db.klein_save_preset(message.from_user.id, preset_name, category, search, priceMax, priceMin, sort_message)
    await message.delete()
    await bot.send_message(message.from_user.id, text=f"Ваш пресет {preset_name} был успешно сохранен!")



@dp.callback_query(lambda callback_query: callback_query.data.startswith("klein_category|"))
async def klein_category_choose(call: types.CallbackQuery, state: klein_states.Klein.category):
    category_keyboards = {
        "transport": klein_kb.klein_transport_categories,
        "services": klein_kb.klein_services_categories,
        "tickets": klein_kb.klein_tickets_categories,
        "electric": klein_kb.klein_electric_categories,
        "kids": klein_kb.klein_family_categories,
        "hobby": klein_kb.klein_hobbies_categories,  # Обновлено
        "garden": klein_kb.klein_garden_categories,
        "pets": klein_kb.klein_pets_categories,
        "property": klein_kb.klein_property_categories,
        "job": klein_kb.klein_job_categories,
        "beauty": klein_kb.klein_beauty_categories,
        "music": klein_kb.klein_music_categories,
        "help": klein_kb.klein_help_categories,
        "courses": klein_kb.klein_courses_categories,
        "trade": klein_kb.klein_trade_categories,
        "all": None
    }

    sacat_dict = {
        "transport": "c210",
        "services": "c297",
        "tickets": "c231",
        "electric": "c161",
        "kids": "c17",
        "hobby": "c185",
        "garden": "c80",
        "pets": "c130",
        "property": "c195",
        "job": "c102",
        "beauty": "c153",
        "music": "c73",
        "help": "c400",
        "courses": "c235",
        "trade": "c272",
        "all": "all"
    }
    category = call.data.split('|')[1]
    sacat = sacat_dict.get(category)
    if category == "all":
        await state.update_data(category=sacat)
        await state.set_state(klein_states.Klein.search)
        await bot.send_message(call.from_user.id, text=f"Категория {category} была выбрана, введите поисковый запрос")
    else:
        keyboard = category_keyboards.get(category)
        await call.message.delete()
        if keyboard:
            await bot.send_message(call.from_user.id, text=f"Категория {category} была выбрана, выберите подкатегорию",
                                   reply_markup=keyboard)


@dp.callback_query(lambda callback_query: callback_query.data.startswith("klein_transport|"))
async def klein_auto_category(call: types.CallbackQuery, state: klein_states.Klein.category):
    sacat_dict = {
        "auto": "c216",
        "tires": "c223",
        "boats": "c211",
        "bicycles": "c217",
        "motorcycles": "c305",
        "motorcycle_parts": "c306",
        "trucks_and_trailers": "c276",
        "repairs_and_services": "c280",
        "motorhomes": "c220",
        "other_auto_bike_boat": "c241",
        "transport": "c210"
    }
    category = call.data.split('|')[1]
    sacat = sacat_dict.get(category)
    await state.update_data(category=sacat)
    await state.set_state(klein_states.Klein.search)
    await bot.send_message(call.from_user.id, text=f"Категория {category} была выбрана, введите поисковый запрос")


@dp.callback_query(lambda callback_query: callback_query.data.startswith("klein_services|"))
async def klein_services_category(call: types.CallbackQuery, state: klein_states.Klein.category):
    sacat_dict = {
        "senior_care": "c288",
        "auto_bike_boat": "c289",
        "babysitter_childcare": "c290",
        "electronics": "c293",
        "home_and_garden": "c291",
        "artists_musicians": "c292",
        "travel_and_events": "c294",
        "pet_care_training": "c295",
        "moving_and_transport": "c296",
        "other_services": "c298",
        "services": "c297"
    }
    category = call.data.split('|')[1]
    sacat = sacat_dict.get(category)
    await state.update_data(category=sacat)
    await state.set_state(klein_states.Klein.search)
    await bot.send_message(call.from_user.id, text=f"Категория {category} была выбрана, введите поисковый запрос")


@dp.callback_query(lambda callback_query: callback_query.data.startswith("klein_tickets|"))
async def klein_tickets_category(call: types.CallbackQuery, state: klein_states.Klein.category):
    sacat_dict = {
        "trains_public_transport": "c286",
        "comedy_kabarett": "c254",
        "vouchers": "c287",
        "kids": "c252",
        "concerts": "c255",
        "sports": "c257",
        "theater_musicals": "c251",
        "other_tickets": "c256",
        "tickets": "c231"
    }
    category = call.data.split('|')[1]
    sacat = sacat_dict.get(category)
    await state.update_data(category=sacat)
    await state.set_state(klein_states.Klein.search)
    await bot.send_message(call.from_user.id, text=f"Категория {category} была выбрана, введите поисковый запрос")


@dp.callback_query(lambda callback_query: callback_query.data.startswith("klein_electric|"))
async def klein_electric_category(call: types.CallbackQuery, state: klein_states.Klein.category):
    sacat_dict = {
        "audio_hifi": "c172",
        "electronic_services": "c226",
        "photo": "c245",
        "phones": "c173",
        "appliances": "c176",
        "consoles": "c279",
        "laptops": "c278",
        "pcs": "c228",
        "pc_accessories_software": "c225",
        "tablets_readers": "c285",
        "tv_video": "c175",
        "video_games": "c227",
        "other_electronics": "c168",
        "electric": "c161"
    }
    category = call.data.split('|')[1]
    sacat = sacat_dict.get(category)
    await state.update_data(category=sacat)
    await state.set_state(klein_states.Klein.search)
    await bot.send_message(call.from_user.id, text=f"Категория {category} была выбрана, введите поисковый запрос")


@dp.callback_query(lambda callback_query: callback_query.data.startswith("klein_family|"))
async def klein_family_category(call: types.CallbackQuery, state: klein_states.Klein.category):
    sacat_dict = {
        "elderly_care": "c236",
        "childrens_clothing": "c22",
        "childrens_shoes": "c19",
        "baby_products": "c258",
        "child_car_seats": "c21",
        "babysitter_and_childcare": "c237",
        "strollers_and_buggies": "c25",
        "childrens_furniture": "c20",
        "toys": "c23",
        "other_family_and_children_products": "c18",
        "family": "c17"
    }
    category = call.data.split('|')[1]
    sacat = sacat_dict.get(category)
    await state.update_data(category=sacat)
    await state.set_state(klein_states.Klein.search)
    await bot.send_message(call.from_user.id, text=f"Категория {category} была выбрана, введите поисковый запрос")



@dp.callback_query(lambda callback_query: callback_query.data.startswith("klein_hobbies|"))
async def klein_hobbies_category(call: types.CallbackQuery, state: klein_states.Klein.category):
    sacat_dict = {
        "esoteric_spiritual": "c232",
        "food_and_drinks": "c248",
        "free_time_activities": "c187",
        "handcraft_crafts": "c282",
        "art_antiques": "c240",
        "artist_musician": "c191",
        "modelling": "c249",
        "travel_event_services": "c233",
        "collect": "c234",
        "sport_camping": "c230",
        "junk": "c250",
        "found_lost": "c189",
        "another_hobbies": "c242",
        "hobbies": "c185",
    }
    category = call.data.split('|')[1]
    sacat = sacat_dict.get(category)
    await state.update_data(category=sacat)
    await state.set_state(klein_states.Klein.search)
    await bot.send_message(call.from_user.id, text=f"Категория {category} была выбрана, введите поисковый запрос")


@dp.callback_query(lambda callback_query: callback_query.data.startswith("klein_garden|"))
async def klein_garden_category(call: types.CallbackQuery, state: klein_states.Klein.category):
    sacat_dict = {
        "bathroom": "c91",
        "office": "c93",
        "decoration": "c246",
        "services": "c239",
        "garden_accessories": "c89",
        "home_textiles": "c90",
        "home_improvement": "c84",
        "kitchen_dining": "c86",
        "lamps_lighting": "c82",
        "bedroom": "c81",
        "living_room": "c88",
        "other_home_garden": "c87",
        "garden": "c80",
    }
    category = call.data.split('|')[1]
    sacat = sacat_dict.get(category)
    await state.update_data(category=sacat)
    await state.set_state(klein_states.Klein.search)
    await bot.send_message(call.from_user.id, text=f"Категория {category} была выбрана, введите поисковый запрос")


@dp.callback_query(lambda callback_query: callback_query.data.startswith("klein_pets|"))
async def klein_pets_category(call: types.CallbackQuery, state: klein_states.Klein.category):
    sacat_dict = {
        "fish": "c138",
        "dogs": "c134",
        "cats": "c136",
        "small_animals": "c132",
        "livestock": "c135",
        "horses": "c139",
        "pet_care_and_training": "c133",
        "lost_pets": "c283",
        "birds": "c243",
        "accessories": "c313",
        "pets": "c130",
    }
    category = call.data.split('|')[1]
    sacat = sacat_dict.get(category)
    await state.update_data(category=sacat)
    await state.set_state(klein_states.Klein.search)
    await bot.send_message(call.from_user.id, text=f"Категория {category} была выбрана, введите поисковый запрос")


@dp.callback_query(lambda callback_query: callback_query.data.startswith("klein_property|"))
async def klein_property_category(call: types.CallbackQuery, state: klein_states.Klein.category):
    sacat_dict = {
        "temporary_and_wg": "c199",
        "condos": "c196",
        "holiday_and_foreign_properties": "c275",
        "garages_and_parking_spaces": "c197",
        "commercial_properties": "c277",
        "plots_and_gardens": "c207",
        "houses_for_sale": "c208",
        "houses_for_rent": "c205",
        "apartments_for_rent": "c203",
        "moving_and_transport": "c238",
        "other_properties": "c198",
        "property": "c195",
    }
    category = call.data.split('|')[1]
    sacat = sacat_dict.get(category)
    await state.update_data(category=sacat)
    await state.set_state(klein_states.Klein.search)
    await bot.send_message(call.from_user.id, text=f"Категория {category} была выбрана, введите поисковый запрос")


@dp.callback_query(lambda callback_query: callback_query.data.startswith("klein_job|"))
async def klein_job_category(call: types.CallbackQuery, state: klein_states.Klein.category):
    sacat_dict = {
        "training": "c118",
        "construction": "c111",
        "office_administration": "c114",
        "gastronomy_tourism": "c110",
        "customer_service": "c105",
        "mini_jobs": "c107",
        "internships": "c125",
        "social_care": "c123",
        "transport_logistics": "c247",
        "sales_purchases": "c117",
        "other_jobs": "c109",
        "job": "c102",
    }
    category = call.data.split('|')[1]
    sacat = sacat_dict.get(category)
    await state.update_data(category=sacat)
    await state.set_state(klein_states.Klein.search)
    await bot.send_message(call.from_user.id, text=f"Категория {category} была выбрана, введите поисковый запрос")


@dp.callback_query(lambda callback_query: callback_query.data.startswith("klein_beauty|"))
async def klein_beauty_category(call: types.CallbackQuery, state: klein_states.Klein.category):
    sacat_dict = {
        "accessories_jewelry": "c156",
        "beauty_health": "c224",
        "women_clothing": "c154",
        "women_shoes": "c159",
        "men_clothing": "c160",
        "men_shoes": "c158",
        "watches_jewelry": "c157",
        "other_fashion_beauty": "c155",
        "beauty": "c153",
    }
    category = call.data.split('|')[1]
    sacat = sacat_dict.get(category)
    await state.update_data(category=sacat)
    await state.set_state(klein_states.Klein.search)
    await bot.send_message(call.from_user.id, text=f"Категория {category} была выбрана, введите поисковый запрос")


@dp.callback_query(lambda callback_query: callback_query.data.startswith("klein_music|"))
async def klein_music_category(call: types.CallbackQuery, state: klein_states.Klein.category):
    sacat_dict = {
        "books_and_magazines": "c153",
        "office_and_stationery": "c281",
        "comics": "c284",
        "textbooks_school_study": "c77",
        "movies_and_dvd": "c79",
        "music_and_cds": "c78",
        "musical_instruments": "c74",
        "other_music_movies_books": "c75",
        "music": "c73",
    }
    category = call.data.split('|')[1]
    sacat = sacat_dict.get(category)
    await state.update_data(category=sacat)
    await state.set_state(klein_states.Klein.search)
    await bot.send_message(call.from_user.id, text=f"Категория {category} была выбрана, введите поисковый запрос")


@dp.callback_query(lambda callback_query: callback_query.data.startswith("klein_help|"))
async def klein_help_category(call: types.CallbackQuery, state: klein_states.Klein.category):
    sacat_dict = {
        "neighborhood_assistance": "c401",
        "help": "c400",
    }
    category = call.data.split('|')[1]
    sacat = sacat_dict.get(category)
    await state.update_data(category=sacat)
    await state.set_state(klein_states.Klein.search)
    await bot.send_message(call.from_user.id, text=f"Категория {category} была выбрана, введите поисковый запрос")


@dp.callback_query(lambda callback_query: callback_query.data.startswith("klein_courses|"))
async def klein_courses_category(call: types.CallbackQuery, state: klein_states.Klein.category):
    sacat_dict = {
        "beauty_health": "c269",
        "computer_courses": "c260",
        "esoteric_spiritual": "c265",
        "cooking_baking": "c263",
        "art_design": "c264",
        "music_singing": "c262",
        "tutoring": "c268",
        "sports_courses": "c261",
        "language_courses": "c271",
        "dance_courses": "c267",
        "further_education": "c266",
        "other_lessons_courses": "c270",
        "lessons": "c235"
    }
    category = call.data.split('|')[1]
    sacat = sacat_dict.get(category)
    await state.update_data(category=sacat)
    await state.set_state(klein_states.Klein.search)
    await bot.send_message(call.from_user.id, text=f"Категория {category} была выбрана, введите поисковый запрос")


@dp.callback_query(lambda callback_query: callback_query.data.startswith("klein_trade|"))
async def klein_trade_category(call: types.CallbackQuery, state: klein_states.Klein.category):
    sacat_dict = {
        "exchange": "c273",
        "loans": "c274",
        "giveaway": "c192",
        "trade": "c272",
    }
    category = call.data.split('|')[1]
    sacat = sacat_dict.get(category)
    await state.update_data(category=sacat)
    await state.set_state(klein_states.Klein.search)
    await bot.send_message(call.from_user.id, text=f"Категория {category} была выбрана, введите поисковый запрос")


@dp.message(StateFilter(klein_states.Klein.search))
async def klein_search(message: types.Message, state: klein_states.Klein.search):
    search_param = message.text
    await state.update_data(search=search_param)
    await bot.send_message(message.from_user.id,
                           text="Введите параметр максимальной цены для парсинга, чтобы оставить по умолчанию введите 'def'")
    await state.set_state(klein_states.Klein.priceMax)


@dp.message(StateFilter(klein_states.Klein.priceMax))
async def klein_price_max(message: types.Message, state: klein_states.Klein.priceMax):
    try:
        priceMax = message.text
        await state.update_data(priceMax=priceMax)
        await bot.send_message(message.from_user.id,
                               text="Введите параметр минимальной цены для парсинга, чтобы оставить по умолчанию введите 'def'")
        await state.set_state(klein_states.Klein.priceMin)
    except ValueError:
        await bot.send_message(message.from_user.id, text="Пожалуйста, введите корректное число для 'priceMax'.")


@dp.message(StateFilter(klein_states.Klein.priceMin))
async def klein_price_max(message: types.Message, state: klein_states.Klein.priceMin):
    try:
        priceMin = message.text
        await state.update_data(priceMin=priceMin)
        await bot.send_message(message.from_user.id,
                               text="Введите параметр сортировки для парсинга (например, 'по дате создания','по возрастанию цены'):")
        await state.set_state(klein_states.Klein.sort)
    except ValueError:
        await bot.send_message(message.from_user.id, text="Пожалуйста, введите корректное число для 'priceMin'.")


@dp.message(StateFilter(klein_states.Klein.sort))
async def klein_sort(message: Message, state: klein_states.Klein.sort):
    sort = message.text
    await state.update_data(sort=sort)
    await bot.send_message(message.from_user.id, text="Введите количество товаров для вывода (максимум 80)")
    await state.set_state(klein_states.Klein.quantity)


@dp.message(StateFilter(klein_states.Klein.quantity))
async def get_klein_quantity_for_categories(message: types.Message, state: klein_states.Klein.quantity):
    quantity = message.text
    await state.update_data(quantity=quantity)
    user_data = await state.get_data()
    search = user_data.get('search')
    search = search.replace(" ", "-")
    priceMax = user_data.get('priceMax')
    priceMin = user_data.get('priceMin')
    sort = user_data.get('sort')
    quantity = user_data.get('quantity')
    category = user_data.get("category")
    sort_message = None
    if search == "1" or search is None:
        search = "bicycle"
    else:
        search = search.replace(" ", "-")
    if priceMax == "def" or priceMax is None or not priceMax.isdigit():
        priceMax = 500
    if priceMin == "def" or priceMin is None or not priceMax.isdigit():
        priceMin = 50
    if quantity is None or int(quantity) > 80 or int(quantity) < 0 or not quantity.isdigit():
        quantity = 25
    if sort == "по дате создания" or sort == "По дате создания":
        sort = ""
        sort_message = "По дате создания"
    elif sort == "по возрастанию цены" or sort == "По возрастанию цены":
        sort = "sortierung:preis"
        sort_message = "По возрастанию цены"
    else:
        sort = ""
        sort_message = "По дате создания"



    await bot.send_message(message.from_user.id, text=f'<b>Хотите ли вы сохранить эти настройки?</b>\n\n\n'
                                                      f'<b>Ваши настройки:</b>\n\n '
                                                      f'Категория: {category}\n'
                                                      f'Поисковый запрос: {search}\n'
                                                      f'Максимальная цена: {priceMax}\n'
                                                      f'Минимальная цена: {priceMin}\n'
                                                      f'Сортировка: {sort_message}',
                           reply_markup=klein_kb.klein_preset_save, parse_mode="HTML")

    async def run_klein_parsing(user_id, category, search, priceMax, priceMin, sort, quantity):
        try:
            await klein.klein_parsing_with_filters(user_id, category, search, priceMax, priceMin, sort, quantity)
            await bot.send_message(message.from_user.id, text="Парсинг был завершен!")
        except Exception as e:
            logging.error(f'Ошибка во время парсинга: {e}')
            await bot.send_message(message.from_user.id,
                                   text="Произошла ошибка во время парсинга. Пожалуйста, попробуйте снова позже.")

    loop.create_task(run_klein_parsing(message.from_user.id, category, search, priceMax, priceMin, sort, quantity))

    async def display_klein_status(quantity):
        report_message = f"<b>Парсинг начал работу:</b> \n\n\n" \
                         f"Сервис: <b>Kleinanzeigen</b> \n\n" \
                         f"Количество спаршенных данных: 0\n\n" \
                         f"Количество сообщений для отправки: {quantity}\n\n" \
                         f"Выберите дальнейшие действия: "

        try:
            await bot.send_message(message.from_user.id, text="Парсинг запущен, ожидайте")
            await message.delete()
            sent_message = await bot.send_message(message.from_user.id,
                                                  text=report_message,
                                                  reply_markup=kb.klein_after_parsing,
                                                  disable_web_page_preview=True,
                                                  parse_mode="HTML")

            await bot.pin_chat_message(chat_id=message.from_user.id,
                                       message_id=sent_message.message_id)
        except Exception as e:
            logging.error(f'Ошибка при обновлении сообщения: {e}')

    asyncio.create_task(display_klein_status(quantity))


@dp.message(StateFilter(klein_states_url.KleinUrl.url))
async def get_klein_url(message: types.Message, state: klein_states_url.KleinUrl.url):
    url = message.text
    await state.update_data(url=url)
    await message.delete()
    await bot.send_message(message.from_user.id, text="Введите количество товаров для вывода (максимум 80)")
    await state.set_state(klein_states_url.KleinUrl.quantity)


@dp.message(StateFilter(klein_states_url.KleinUrl.quantity))
async def get_klein_quantity_url(message: types.Message, state: klein_states.Klein.quantity):
    quantity = message.text
    await state.update_data(quantity=quantity)
    user_data = await state.get_data()
    url = user_data.get("url")
    if quantity is None or int(quantity) > 80 or int(quantity) < 0 or not quantity.isdigit():
        quantity = 25
    if "https://www.kleinanzeigen.de/" in url:
        async def run_klein_parser_url(user_id, url, quantity):
            try:
                await klein.klein_parser_url(user_id, url, quantity)
                await bot.send_message(message.from_user.id, text="Парсинг завершен!")
            except Exception as e:
                logging.error(f'Ошибка во время парсинга: {e}')
                await bot.send_message(message.from_user.id,
                                       text="Произошла ошибка во время парсинга. Пожалуйста, попробуйте снова позже.")

        loop.create_task(run_klein_parser_url(message.from_user.id, url, quantity))

        async def display_klein_status(url, quantity):
            try:
                await bot.send_message(message.from_user.id, text="Парсинг запущен, ожидайте")
                await message.delete()
                sent_message = await bot.send_message(message.from_user.id, text="<b>Парсинг начал работу:</b> \n\n\n"
                                                                                 f"Ссылка для парсинга:\n {url}\n\n"
                                                                                 f"Количество спаршенных данных: 0\n\n"
                                                                                 f"Количество сообщений для отправки: {quantity}\n\n"
                                                                                 f"Выберите дальнейшие действия: ",
                                                      reply_markup=kb.klein_after_parsing,
                                                      disable_web_page_preview=True,
                                                      parse_mode="HTML")

                await bot.pin_chat_message(chat_id=message.from_user.id,
                                           message_id=sent_message.message_id)

                logging.info('Это сообщение будет записано в файл bot.log')
            except Exception as e:
                logging.error(f'Ошибка во время отправки сообщения {e}')

        asyncio.create_task(display_klein_status(url, quantity))


@dp.callback_query(lambda callback_query: callback_query.data in ["klein_json", "klein_message", "klein_send_messages",
                                                                  "seller_date_sorting", "update_parser_status",
                                                                  "seller_feedback_delete", "delete_without_sipping"])
async def klein_after_parsing_choice(call: types.CallbackQuery, state: klein_states.Klein.quantity):
    if call.data == "klein_json":
        await bot.send_message(call.from_user.id, text="JSON файл отправляется...")
        parser_output_file = FSInputFile(path='services/kleinanzeigen/klein_output.json', filename='klein_output.json')
        await bot.send_document(call.from_user.id, document=parser_output_file)
    elif call.data == "klein_message":
        user_data = await state.get_data()
        quantity = user_data.get("quantity")
        if quantity is None or int(quantity) > 80 or int(quantity) < 0 or not quantity.isdigit():
            quantity = 25
        output = await klein_parser_output.output_klein(user_id=call.from_user.id)
        items_number = int(quantity)
        for item in itertools.islice(output, items_number):
            await bot.send_message(call.from_user.id, item, parse_mode="HTML")
    elif call.data == "klein_send_messages":
        await bot.send_message(call.from_user.id, text="Функция в разработке!")
    elif call.data == "seller_date_sorting":
        await klein_parser_output.sort_items_by_registration_date()
        await bot.send_message(call.from_user.id, text="Данные были отсортированны по дате регистрации продавца")
    elif call.data == "update_parser_status":
        async def update_klein_status():
            user_data = await state.get_data()
            quantity = user_data.get("quantity")
            if quantity is None or int(quantity) > 80 or int(quantity) < 0 or not quantity.isdigit():
                quantity = 25
            collected_items = await klein_parser_output.klein_number_of_items()
            await call.message.delete()
            report_message = f"<b>Отчет о парсинге:</b> \n\n\n" \
                             f"Сервис: <b>Kleinanzeigen</b> \n\n" \
                             f"Количество спаршенных данных: {collected_items}\n\n" \
                             f"Количество сообщений для отправки: {quantity}\n\n" \
                             f"<b>Если вы удаляли или сортировали файлы во время парсинга, то рекомендуется повторить процедуру после завершения парсинга</b>\n\n\n" \
                             f"Выберите дальнейшие действия: "

            try:
                sent_message = await bot.send_message(call.from_user.id,
                                                      text=report_message,
                                                      reply_markup=kb.klein_after_parsing,
                                                      disable_web_page_preview=True,
                                                      parse_mode="HTML")

                await bot.pin_chat_message(chat_id=call.from_user.id,
                                           message_id=sent_message.message_id)
            except Exception as e:
                logging.error(f'Ошибка при обновлении сообщения: {e}')

        await update_klein_status()

    elif call.data == "seller_feedback_delete":
        await klein_parser_output.delete_items_with_rating()
        collected_items = await klein_parser_output.klein_number_of_items()
        await bot.send_message(call.from_user.id, text=f"Товары с высоким рейтингом продавца были удалены из JSON файла\n\n"
                                                       f"Осталось товаров: {collected_items}")

    elif call.data == "delete_without_sipping":
        await klein_parser_output.delete_items_without_shipping()
        collected_items = await klein_parser_output.klein_number_of_items()
        await bot.send_message(call.from_user.id, text=f"Товары без доставки были удалены из JSON файла\n\n"
                                                       f"Осталось товаров: {collected_items}")


@dp.callback_query(lambda callback_query: callback_query.data.startswith('ETSY_'))
async def etsy_handler(call: types.CallbackQuery):
    call_data = call.data.split("_")[1]
    if call.data == f"ETSY_{call_data}":
        qwer = 1






@dp.callback_query(lambda callback_query: callback_query.data == 'configurator')
async def configurator_handler(callback_query: types.CallbackQuery):
    if callback_query.data == 'configurator':
        configurator_kb = await kb.get_settings_kb(callback_query.from_user.id)
        output = await settings_out.output_settings(callback_query.from_user.id)
        for item in output:
            message = await bot.send_message(callback_query.from_user.id,
                                             text=f"<b>Конфигуратор объявлений:</b>\n\n{item}",
                                             reply_markup=configurator_kb, parse_mode="HTML",
                                             disable_web_page_preview=True)
            message = message.message_id
            await db.update_message_id(callback_query.from_user.id, message)
            logging.info('Это сообщение будет записано в файл bot.log')


@dp.callback_query(lambda callback_query: callback_query.data in ['item_name_on', 'item_price_on', 'item_seller_on',
                                                                  'item_location_on', 'item_description_on',
                                                                  'item_picture_on', 'item_publish_date_on',
                                                                  'item_views_on', 'seller_registration_date_on',
                                                                  'seller_items_number_on', 'item_extra_info_on',
                                                                  'output_files_on'])
async def output_settings_off(callback_query: types.CallbackQuery):
    if callback_query.data == "item_name_on":
        await db.turn_off_user_setting(user_id=callback_query.from_user.id, setting="item_name")
        message_id = await db.get_message_id(callback_query.from_user.id)
        message_id = message_id[0][0]
        configurator_kb = await kb.get_settings_kb(callback_query.from_user.id)
        output = await settings_out.output_settings(callback_query.from_user.id)
        for item in output:
            await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=message_id,
                                        text=f"<b>Конфигуратор объявлений:</b>\n\n{item}", reply_markup=configurator_kb,
                                        parse_mode="HTML", disable_web_page_preview=True)
            logging.info('Это сообщение будет записано в файл bot.log')
    elif callback_query.data == "item_price_on":
        await db.turn_off_user_setting(user_id=callback_query.from_user.id, setting="item_price")
        message_id = await db.get_message_id(callback_query.from_user.id)
        message_id = message_id[0][0]
        configurator_kb = await kb.get_settings_kb(callback_query.from_user.id)
        output = await settings_out.output_settings(callback_query.from_user.id)
        for item in output:
            await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=message_id,
                                        text=f"<b>Конфигуратор объявлений:</b>\n\n{item}", reply_markup=configurator_kb,
                                        parse_mode="HTML", disable_web_page_preview=True)
            logging.info('Это сообщение будет записано в файл bot.log')
    elif callback_query.data == "item_seller_on":
        await db.turn_off_user_setting(user_id=callback_query.from_user.id, setting="item_seller")
        message_id = await db.get_message_id(callback_query.from_user.id)
        message_id = message_id[0][0]
        configurator_kb = await kb.get_settings_kb(callback_query.from_user.id)
        output = await settings_out.output_settings(callback_query.from_user.id)
        for item in output:
            await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=message_id,
                                        text=f"<b>Конфигуратор объявлений:</b>\n\n{item}", reply_markup=configurator_kb,
                                        parse_mode="HTML", disable_web_page_preview=True)
            logging.info('Это сообщение будет записано в файл bot.log')
    elif callback_query.data == "item_location_on":
        await db.turn_off_user_setting(user_id=callback_query.from_user.id, setting="item_location")
        message_id = await db.get_message_id(callback_query.from_user.id)
        message_id = message_id[0][0]
        configurator_kb = await kb.get_settings_kb(callback_query.from_user.id)
        output = await settings_out.output_settings(callback_query.from_user.id)
        for item in output:
            await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=message_id,
                                        text=f"<b>Конфигуратор объявлений:</b>\n\n{item}", reply_markup=configurator_kb,
                                        parse_mode="HTML", disable_web_page_preview=True)
            logging.info('Это сообщение будет записано в файл bot.log')
    elif callback_query.data == "item_description_on":
        await db.turn_off_user_setting(user_id=callback_query.from_user.id, setting="item_description")
        message_id = await db.get_message_id(callback_query.from_user.id)
        message_id = message_id[0][0]
        configurator_kb = await kb.get_settings_kb(callback_query.from_user.id)
        output = await settings_out.output_settings(callback_query.from_user.id)
        for item in output:
            await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=message_id,
                                        text=f"<b>Конфигуратор объявлений:</b>\n\n{item}",
                                        reply_markup=configurator_kb,
                                        parse_mode="HTML", disable_web_page_preview=True)
            logging.info('Это сообщение будет записано в файл bot.log')
    elif callback_query.data == "item_picture_on":
        await db.turn_off_user_setting(user_id=callback_query.from_user.id, setting="item_picture")
        message_id = await db.get_message_id(callback_query.from_user.id)
        message_id = message_id[0][0]
        configurator_kb = await kb.get_settings_kb(callback_query.from_user.id)
        output = await settings_out.output_settings(callback_query.from_user.id)
        for item in output:
            await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=message_id,
                                        text=f"<b>Конфигуратор объявлений:</b>\n\n{item}",
                                        reply_markup=configurator_kb,
                                        parse_mode="HTML", disable_web_page_preview=True)
            logging.info('Это сообщение будет записано в файл bot.log')
    elif callback_query.data == "item_publish_date_on":
        await db.turn_off_user_setting(user_id=callback_query.from_user.id, setting="item_publish_date")
        message_id = await db.get_message_id(callback_query.from_user.id)
        message_id = message_id[0][0]
        configurator_kb = await kb.get_settings_kb(callback_query.from_user.id)
        output = await settings_out.output_settings(callback_query.from_user.id)
        for item in output:
            await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=message_id,
                                        text=f"<b>Конфигуратор объявлений:</b>\n\n{item}",
                                        reply_markup=configurator_kb,
                                        parse_mode="HTML", disable_web_page_preview=True)
            logging.info('Это сообщение будет записано в файл bot.log')
    elif callback_query.data == "item_views_on":
        await db.turn_off_user_setting(user_id=callback_query.from_user.id, setting="item_views")
        message_id = await db.get_message_id(callback_query.from_user.id)
        message_id = message_id[0][0]
        configurator_kb = await kb.get_settings_kb(callback_query.from_user.id)
        output = await settings_out.output_settings(callback_query.from_user.id)
        for item in output:
            await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=message_id,
                                        text=f"<b>Конфигуратор объявлений:</b>\n\n{item}",
                                        reply_markup=configurator_kb,
                                        parse_mode="HTML", disable_web_page_preview=True)
            logging.info('Это сообщение будет записано в файл bot.log')
    elif callback_query.data == "seller_registration_date_on":
        await db.turn_off_user_setting(user_id=callback_query.from_user.id, setting="seller_registration_date")
        message_id = await db.get_message_id(callback_query.from_user.id)
        message_id = message_id[0][0]
        configurator_kb = await kb.get_settings_kb(callback_query.from_user.id)
        output = await settings_out.output_settings(callback_query.from_user.id)
        for item in output:
            await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=message_id,
                                        text=f"<b>Конфигуратор объявлений:</b>\n\n{item}",
                                        reply_markup=configurator_kb,
                                        parse_mode="HTML", disable_web_page_preview=True)
            logging.info('Это сообщение будет записано в файл bot.log')
    elif callback_query.data == "seller_items_number_on":
        await db.turn_off_user_setting(user_id=callback_query.from_user.id, setting="seller_items_number")
        message_id = await db.get_message_id(callback_query.from_user.id)
        message_id = message_id[0][0]
        configurator_kb = await kb.get_settings_kb(callback_query.from_user.id)
        output = await settings_out.output_settings(callback_query.from_user.id)
        for item in output:
            await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=message_id,
                                        text=f"<b>Конфигуратор объявлений:</b>\n\n{item}",
                                        reply_markup=configurator_kb,
                                        parse_mode="HTML", disable_web_page_preview=True)
            logging.info('Это сообщение будет записано в файл bot.log')
    elif callback_query.data == "item_extra_info_on":
        await db.turn_off_user_setting(user_id=callback_query.from_user.id, setting="item_extra_info")
        message_id = await db.get_message_id(callback_query.from_user.id)
        message_id = message_id[0][0]
        configurator_kb = await kb.get_settings_kb(callback_query.from_user.id)
        output = await settings_out.output_settings(callback_query.from_user.id)
        for item in output:
            await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=message_id,
                                        text=f"<b>Конфигуратор объявлений:</b>\n\n{item}",
                                        reply_markup=configurator_kb,
                                        parse_mode="HTML", disable_web_page_preview=True)
            logging.info('Это сообщение будет записано в файл bot.log')
    elif callback_query.data == "output_files_on":
        await db.turn_off_user_setting(user_id=callback_query.from_user.id, setting="output_files")
        message_id = await db.get_message_id(callback_query.from_user.id)
        message_id = message_id[0][0]
        configurator_kb = await kb.get_settings_kb(callback_query.from_user.id)
        output = await settings_out.output_settings(callback_query.from_user.id)
        for item in output:
            await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=message_id,
                                        text=f"<b>Конфигуратор объявлений:</b>\n\n{item}",
                                        reply_markup=configurator_kb,
                                        parse_mode="HTML", disable_web_page_preview=True)
            logging.info('Это сообщение будет записано в файл bot.log')


@dp.callback_query(lambda callback_query: callback_query.data in ['item_name_off', 'item_price_off', 'item_seller_off',
                                                                  'item_location_off', 'item_description_off',
                                                                  'item_picture_off', 'item_publish_date_off',
                                                                  'item_views_off', 'seller_registration_date_off',
                                                                  'seller_items_number_off', 'item_extra_info_off',
                                                                  'output_files_off'])
async def output_settings_on(callback_query: types.CallbackQuery):
    if callback_query.data == "item_name_off":
        await db.turn_on_user_setting(user_id=callback_query.from_user.id, setting="item_name")
        message_id = await db.get_message_id(callback_query.from_user.id)
        message_id = message_id[0][0]
        configurator_kb = await kb.get_settings_kb(callback_query.from_user.id)
        output = await settings_out.output_settings(callback_query.from_user.id)
        for item in output:
            await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=message_id,
                                        text=f"<b>Конфигуратор объявлений:</b>\n\n{item}", reply_markup=configurator_kb,
                                        parse_mode="HTML", disable_web_page_preview=True)
            logging.info('Это сообщение будет записано в файл bot.log')
    elif callback_query.data == "item_price_off":
        await db.turn_on_user_setting(user_id=callback_query.from_user.id, setting="item_price")
        message_id = await db.get_message_id(callback_query.from_user.id)
        message_id = message_id[0][0]
        configurator_kb = await kb.get_settings_kb(callback_query.from_user.id)
        output = await settings_out.output_settings(callback_query.from_user.id)
        for item in output:
            await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=message_id,
                                        text=f"<b>Конфигуратор объявлений:</b>\n\n{item}", reply_markup=configurator_kb,
                                        parse_mode="HTML", disable_web_page_preview=True)
            logging.info('Это сообщение будет записано в файл bot.log')
    elif callback_query.data == "item_seller_off":
        await db.turn_on_user_setting(user_id=callback_query.from_user.id, setting="item_seller")
        message_id = await db.get_message_id(callback_query.from_user.id)
        message_id = message_id[0][0]
        configurator_kb = await kb.get_settings_kb(callback_query.from_user.id)
        output = await settings_out.output_settings(callback_query.from_user.id)
        for item in output:
            await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=message_id,
                                        text=f"<b>Конфигуратор объявлений:</b>\n\n{item}", reply_markup=configurator_kb,
                                        parse_mode="HTML", disable_web_page_preview=True)
            logging.info('Это сообщение будет записано в файл bot.log')
    elif callback_query.data == "item_location_off":
        await db.turn_on_user_setting(user_id=callback_query.from_user.id, setting="item_location")
        message_id = await db.get_message_id(callback_query.from_user.id)
        message_id = message_id[0][0]
        configurator_kb = await kb.get_settings_kb(callback_query.from_user.id)
        output = await settings_out.output_settings(callback_query.from_user.id)
        for item in output:
            await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=message_id,
                                        text=f"<b>Конфигуратор объявлений:</b>\n\n{item}", reply_markup=configurator_kb,
                                        parse_mode="HTML", disable_web_page_preview=True)
            logging.info('Это сообщение будет записано в файл bot.log')
    elif callback_query.data == "item_description_off":
        await db.turn_on_user_setting(user_id=callback_query.from_user.id, setting="item_description")
        message_id = await db.get_message_id(callback_query.from_user.id)
        message_id = message_id[0][0]
        configurator_kb = await kb.get_settings_kb(callback_query.from_user.id)
        output = await settings_out.output_settings(callback_query.from_user.id)
        for item in output:
            await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=message_id,
                                        text=f"<b>Конфигуратор объявлений:</b>\n\n{item}", reply_markup=configurator_kb,
                                        parse_mode="HTML", disable_web_page_preview=True)
            logging.info('Это сообщение будет записано в файл bot.log')
    elif callback_query.data == "item_picture_off":
        await db.turn_on_user_setting(user_id=callback_query.from_user.id, setting="item_picture")
        message_id = await db.get_message_id(callback_query.from_user.id)
        message_id = message_id[0][0]
        configurator_kb = await kb.get_settings_kb(callback_query.from_user.id)
        output = await settings_out.output_settings(callback_query.from_user.id)
        for item in output:
            await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=message_id,
                                        text=f"<b>Конфигуратор объявлений:</b>\n\n{item}", reply_markup=configurator_kb,
                                        parse_mode="HTML", disable_web_page_preview=True)
            logging.info('Это сообщение будет записано в файл bot.log')
    elif callback_query.data == "item_publish_date_off":
        await db.turn_on_user_setting(user_id=callback_query.from_user.id, setting="item_publish_date")
        message_id = await db.get_message_id(callback_query.from_user.id)
        message_id = message_id[0][0]
        configurator_kb = await kb.get_settings_kb(callback_query.from_user.id)
        output = await settings_out.output_settings(callback_query.from_user.id)
        for item in output:
            await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=message_id,
                                        text=f"<b>Конфигуратор объявлений:</b>\n\n{item}", reply_markup=configurator_kb,
                                        parse_mode="HTML", disable_web_page_preview=True)
            logging.info('Это сообщение будет записано в файл bot.log')
    elif callback_query.data == "item_views_off":
        await db.turn_on_user_setting(user_id=callback_query.from_user.id, setting="item_views")
        message_id = await db.get_message_id(callback_query.from_user.id)
        message_id = message_id[0][0]
        configurator_kb = await kb.get_settings_kb(callback_query.from_user.id)
        output = await settings_out.output_settings(callback_query.from_user.id)
        for item in output:
            await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=message_id,
                                        text=f"<b>Конфигуратор объявлений:</b>\n\n{item}", reply_markup=configurator_kb,
                                        parse_mode="HTML", disable_web_page_preview=True)
            logging.info('Это сообщение будет записано в файл bot.log')
    elif callback_query.data == "seller_registration_date_off":
        await db.turn_on_user_setting(user_id=callback_query.from_user.id, setting="seller_registration_date")
        message_id = await db.get_message_id(callback_query.from_user.id)
        message_id = message_id[0][0]
        configurator_kb = await kb.get_settings_kb(callback_query.from_user.id)
        output = await settings_out.output_settings(callback_query.from_user.id)
        for item in output:
            await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=message_id,
                                        text=f"<b>Конфигуратор объявлений:</b>\n\n{item}", reply_markup=configurator_kb,
                                        parse_mode="HTML", disable_web_page_preview=True)
            logging.info('Это сообщение будет записано в файл bot.log')
    elif callback_query.data == "seller_items_number_off":
        await db.turn_on_user_setting(user_id=callback_query.from_user.id, setting="seller_items_number")
        message_id = await db.get_message_id(callback_query.from_user.id)
        message_id = message_id[0][0]
        configurator_kb = await kb.get_settings_kb(callback_query.from_user.id)
        output = await settings_out.output_settings(callback_query.from_user.id)
        for item in output:
            await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=message_id,
                                        text=f"<b>Конфигуратор объявлений:</b>\n\n{item}", reply_markup=configurator_kb,
                                        parse_mode="HTML", disable_web_page_preview=True)
            logging.info('Это сообщение будет записано в файл bot.log')
    elif callback_query.data == "item_extra_info_off":
        await db.turn_on_user_setting(user_id=callback_query.from_user.id, setting="item_extra_info")
        message_id = await db.get_message_id(callback_query.from_user.id)
        message_id = message_id[0][0]
        configurator_kb = await kb.get_settings_kb(callback_query.from_user.id)
        output = await settings_out.output_settings(callback_query.from_user.id)
        for item in output:
            await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=message_id,
                                        text=f"<b>Конфигуратор объявлений:</b>\n\n{item}", reply_markup=configurator_kb,
                                        parse_mode="HTML", disable_web_page_preview=True)
            logging.info('Это сообщение будет записано в файл bot.log')
    elif callback_query.data == "output_files_off":
        await db.turn_on_user_setting(user_id=callback_query.from_user.id, setting="output_files")
        message_id = await db.get_message_id(callback_query.from_user.id)
        message_id = message_id[0][0]
        configurator_kb = await kb.get_settings_kb(callback_query.from_user.id)
        output = await settings_out.output_settings(callback_query.from_user.id)
        for item in output:
            await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=message_id,
                                        text=f"<b>Конфигуратор объявлений:</b>\n\n{item}", reply_markup=configurator_kb,
                                        parse_mode="HTML", disable_web_page_preview=True)
            logging.info('Это сообщение будет записано в файл bot.log')


@dp.callback_query(lambda callback_query: callback_query.data == 'deposit')
async def handle_deposit(callback_query: types.CallbackQuery, state: Balance.amount):
    await bot.send_message(callback_query.from_user.id,
                           text='💰 Пополнение баланса\n\n\n — Выберите удобный способ пополнения',
                           reply_markup=kb.payment_method)


@dp.callback_query(lambda callback_query: callback_query.data in ['crypto_bot', 'back_to_start'])
async def crypto_bot_handler(callback_query: types.CallbackQuery, state: Balance.amount):
    if callback_query.data == "crypto_bot":
        crypto_bot_link = "https://t.me/CryptoBot"
        message_text = (
            f'<b><a href="{crypto_bot_link}">⚜️ CryptoBot</a></b>\n\n'
            '— Минимум: <b>0.1 $</b>\n\n'
            '<b>💸 Введите сумму пополнения в долларах</b>'
        )
        await callback_query.message.edit_text(text=message_text, parse_mode='HTML', disable_web_page_preview=True,
                                               reply_markup=kb.back_to_payment_methods)
        await state.set_state(Balance.amount)


    elif callback_query.data == "back_to_start":
        user_sub = await db.get_time_sub(callback_query.from_user.id)
        if user_sub == 0:
            user_sub = "Нет"
        else:
            user_sub = format_timedelta(time_sub_day(user_sub))
        user_bal = await db.get_balance(callback_query.from_user.id)
        if user_bal == 0:
            user_bal = "0"
        else:
            user_bal = str(user_bal)
        await bot.send_message(callback_query.from_user.id,
                               text=f'💼 Профиль 💼 \n\n👤 Ваш никнейм: {callback_query.from_user.full_name}\n\n💰 Ваш текущий баланс: — ' + user_bal + ' $' + '\n\n🚀 Активные подписки: ' + user_sub,
                               reply_markup=kb.profile, parse_mode="HTML")


@dp.message(StateFilter(Balance.amount))
async def change_balance(message: Message, state: Balance.amount):
    try:
        if float(message.text) >= 0.1:
            crypto_bot_link = "https://t.me/CryptoBot"
            message_text = (
                f'<b><a href="{crypto_bot_link}">⚜️ CryptoBot</a></b>\n\n'
                f'— Сумма: <b>{message.text} $</b>\n\n'
                '<b>💸 Выберите валюту, которой хотите оплатить счёт</b>'
            )
            await message.answer(text=message_text, parse_mode='HTML', disable_web_page_preview=True,
                                 reply_markup=kb.get_crypto_bot_currencies())
            await state.update_data(amount=float(message.text))
        else:
            await message.answer(
                '<b>⚠️ Минимум: 0.1 $!<b>'
            )
    except ValueError:
        await message.answer(
            '<b>❗️Сумма для пополнения должна быть в числовом формате!</b>'
        )


@dp.callback_query(lambda callback_query: callback_query.data.startswith('crypto_bot_currency|'))
async def set_payment_crypto_bot(callback_query: types.CallbackQuery, state: Balance.amount):
    try:
        await callback_query.message.delete()
        cryptopay = AioCryptoPay(os.getenv('CRYPTO_BOT'))
        asset = callback_query.data.split('|')[1].upper()
        payment_data = await state.get_data()
        amount = payment_data.get('amount')
        invoice = await cryptopay.create_invoice(
            asset=asset,
            amount=amount
        )
        await cryptopay.close()
        await db.add_payment_crypto_bot(invoice.invoice_id, amount)
        await callback_query.message.answer(
            f'<b>💸 Отправьте {amount} $ <a href="{invoice.pay_url}">по ссылке</a></b>', parse_mode='HTML',
            reply_markup=kb.check_crypto_bot_kb(invoice.pay_url, invoice.invoice_id))
    except Exception:
        await callback_query.message.answer(
            '<b>⚠️ Произошла ошибка!</b>'
        )


@dp.callback_query(lambda callback_query: callback_query.data.startswith('check_crypto_bot'))
async def check_crypto_bot(call: types.CallbackQuery, state: Balance.amount):
    payment = await db.get_payment_crypto_bot(int(call.data.split('|')[1]))
    payment_data = await state.get_data()
    amount = payment_data.get('amount')
    if payment:
        if await cp.check_crypto_bot_invoice(int(call.data.split('|')[1])):
            await db.delete_payment_crypto_bot(int(call.data.split('|')[1]))
            await db.check_balance(call.from_user.id, amount)
            await call.answer(
                '✅ Оплата прошла успешно!',
                show_alert=True
            )
            await call.message.delete()
            await call.message.answer(
                f'<b>💸 Ваш баланс пополнен на сумму {amount} $!</b>', parse_mode='HTML'
            )
            ADMIN_ID = os.getenv("ADMIN_ID")
            ADMIN_ID_LIST = [int(admin_id) for admin_id in ADMIN_ID.split(",")]
            await state.clear()
            for admin in ADMIN_ID_LIST:
                await call.bot.send_message(
                    admin,
                    f'<b><a href="https://t.me/CryptoBot">⚜️ CryptoBot</a></b>\n'
                    f'<b>💸 Обнаружено пополнение от @{call.from_user.username} [<code>{call.from_user.id}</code>] '
                    f'на сумму {amount} $!</b>', parse_mode='HTML'
                )
        else:
            await call.answer(
                '❗️ Вы не оплатили счёт!',
                show_alert=True
            )


@dp.callback_query(lambda callback_query: callback_query.data == 'back_to_balance')
async def back_to_balance(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id,
                           text='💰 Пополнение баланса\n\n\n — Выберите удобный способ пополнения',
                           reply_markup=kb.payment_method)


@dp.callback_query(lambda callback_query: callback_query.data == 'subscribe')
async def handle_subscription(callback_query: types.CallbackQuery):
    subscription_keyboard = await kb.get_subscription_kb()
    await bot.send_message(callback_query.from_user.id,
                           text='💰 Оформление подписки\n\n\n - Выберите срок подписки:',
                           reply_markup=subscription_keyboard)


@dp.callback_query()
async def callback_query_keyboard_subscriptions(callback_query: types.CallbackQuery,
                                                state: subscribe.Subscription.price, ):
    lengths = await db.get_subscription_time()
    if lengths:
        first_length = lengths[0]
        if callback_query.data == f'{first_length}_sub':
            price = await db.get_subscriptions_price()
            first_price = price[0]
            await bot.send_message(callback_query.from_user.id,
                                   text=f'Вы выбрали подписку на {first_length} за {first_price}$')
            subscription = await db.get_time_sub(callback_query.from_user.id)
            if subscription > int(time.time()):
                await bot.send_message(callback_query.from_user.id, text='У вас уже приобретена подписка!')
            else:
                balance = await db.set_time_sub_1day(user_id=callback_query.from_user.id)
                if not balance:
                    await bot.send_message(callback_query.from_user.id, text='Недостаточно средств на балансе!')
                else:
                    await bot.send_message(callback_query.from_user.id, text='Подписка оформлена!')
        second_length = lengths[1]
        if callback_query.data == f'{second_length}_sub':
            price = await db.get_subscriptions_price()
            second_price = price[1]
            await bot.send_message(callback_query.from_user.id,
                                   text=f'Вы выбрали подписку на {second_length} за {second_price}$')
            subscription = await db.get_time_sub(callback_query.from_user.id)
            if subscription > int(time.time()):
                await bot.send_message(callback_query.from_user.id, text='У вас уже приобретена подписка!')
            else:
                balance = await db.set_time_sub_3days(user_id=callback_query.from_user.id)
                if not balance:
                    await bot.send_message(callback_query.from_user.id, text='Недостаточно средств на балансе!')
                else:
                    await bot.send_message(callback_query.from_user.id, text='Подписка оформлена!')
        third_length = lengths[2]
        if callback_query.data == f'{third_length}_sub':
            price = await db.get_subscriptions_price()
            third_price = price[2]
            await bot.send_message(callback_query.from_user.id,
                                   text=f'Вы выбрали подписку на {third_length} за {third_price}$')
            subscription = await db.get_time_sub(callback_query.from_user.id)
            if subscription > int(time.time()):
                await bot.send_message(callback_query.from_user.id, text='У вас уже приобретена подписка!')
            else:
                balance = await db.set_time_sub_1week(user_id=callback_query.from_user.id)
                if not balance:
                    await bot.send_message(callback_query.from_user.id, text='Недостаточно средств на балансе!')
                else:
                    await bot.send_message(callback_query.from_user.id, text='Подписка оформлена!')
        fourth_length = lengths[3]
        if callback_query.data == f'{fourth_length}_sub':
            price = await db.get_subscriptions_price()
            fourth_price = price[3]
            await bot.send_message(callback_query.from_user.id,
                                   text=f'Вы выбрали подписку на {fourth_length} за {fourth_price}$')
            subscription = await db.get_time_sub(callback_query.from_user.id)
            if subscription > int(time.time()):
                await bot.send_message(callback_query.from_user.id, text='У вас уже приобретена подписка!')
            else:
                balance = await db.set_time_sub_1month(user_id=callback_query.from_user.id)
                if not balance:
                    await bot.send_message(callback_query.from_user.id, text='Недостаточно средств на балансе!')
                else:
                    await bot.send_message(callback_query.from_user.id, text='Подписка оформлена!')
        length = await db.get_subscription_time()
        if length:
            first_sub_length = length[0]
            if callback_query.data == f'{first_sub_length}_sub_edit':
                price = await db.get_subscriptions_price()
                first_sub_price = price[0]
                await bot.send_message(callback_query.from_user.id,
                                       text=f'Вы выбрали подписку на {first_sub_length} за {first_sub_price}$ для ИЗМЕНЕНИЯ ЦЕНЫ')
                await bot.send_message(callback_query.from_user.id,
                                       text=f'Напишите какую цену вы хотите для подписки на {first_sub_length}:')
                await state.set_state(subscribe.Subscription.length)
                await state.update_data(length=first_sub_length)
                await state.set_state(subscribe.Subscription.price)
        length = await db.get_subscription_time()
        if length:
            second_sub_length = length[1]
            if callback_query.data == f'{second_sub_length}_sub_edit':
                price = await db.get_subscriptions_price()
                second_sub_price = price[1]
                await bot.send_message(callback_query.from_user.id,
                                       text=f'Вы выбрали подписку на {second_sub_length} за {second_sub_price}$ для ИЗМЕНЕНИЯ ЦЕНЫ')
                await bot.send_message(callback_query.from_user.id,
                                       text=f'Напишите какую цену вы хотите для подписки на {second_sub_length}:')
                await state.set_state(subscribe.Subscription.length)
                await state.update_data(length=second_sub_length)
                await state.set_state(subscribe.Subscription.price)
        length = await db.get_subscription_time()
        if length:
            third_sub_length = length[2]
            if callback_query.data == f'{third_sub_length}_sub_edit':
                price = await db.get_subscriptions_price()
                third_sub_price = price[2]
                await bot.send_message(callback_query.from_user.id,
                                       text=f'Вы выбрали подписку на {third_sub_length} за {third_sub_price}$ для ИЗМЕНЕНИЯ ЦЕНЫ')
                await bot.send_message(callback_query.from_user.id,
                                       text=f'Напишите какую цену вы хотите для подписки на {third_sub_length}:')
                await state.set_state(subscribe.Subscription.length)
                await state.update_data(length=third_sub_length)
                await state.set_state(subscribe.Subscription.price)
        length = await db.get_subscription_time()
        if length:
            fourth_sub_length = length[3]
            if callback_query.data == f'{fourth_sub_length}_sub_edit':
                price = await db.get_subscriptions_price()
                fourth_sub_price = price[3]
                await bot.send_message(callback_query.from_user.id,
                                       text=f'Вы выбрали подписку на {fourth_sub_length} за {fourth_sub_price}$ для ИЗМЕНЕНИЯ ЦЕНЫ')
                await bot.send_message(callback_query.from_user.id,
                                       text=f'Напишите какую цену вы хотите для подписки на {fourth_sub_length}:')
                await state.set_state(subscribe.Subscription.length)
                await state.update_data(length=fourth_sub_length)
                await state.set_state(subscribe.Subscription.price)


@dp.message(StateFilter(subscribe.Subscription.price))
async def change_sub_time(message: Message, state: subscribe.Subscription.price):
    data = await state.get_data()
    length = data.get('length')
    await state.update_data(answer=message.text)
    answer = message.text
    if not answer.isdigit():
        await message.reply('Напишите сумму в цифровом виде, попробуйте еще раз', reply_markup=kb.admin_panel)
        return
    await db.change_subscription_price(new_price=answer, length=length)
    await state.clear()
    await message.answer('Цена подписки изменена', reply_markup=kb.main)


async def main():
    await dp.start_polling(bot, on_startup=on_startup(), skip_updates=True)


if __name__ == '__main__':
    spider_DEPOP_AU_done_event = asyncio.Event()
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        pass
