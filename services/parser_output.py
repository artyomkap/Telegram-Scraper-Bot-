from datetime import datetime
import json

from aiogram.client import bot
from aiogram.handlers import callback_query
from aiogram.types import FSInputFile

from app import database as db



async def output_depop_au(user_id):
    user_settings = await db.check_user_settings(user_id)

    with open('scraped_data_depop.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    output_data = []
    for item in data:
        output_item = {} # Создаем новый словарь для каждого товара в JSON
        for setting in user_settings:
            if setting[1] == 1:
                output_item["<b>Название товара</b>"] = item.get("Slug")
                output_item["<b>Ссылка на товар</b>"] = item.get("Item Link")
            if setting[2] == 1:
                output_item["<b>Цена товара</b>"] = item.get("Price"), item.get("Currency")
            if setting[3] == 1:
                output_item["<b>Имя продавца</b>"] = item.get("Seller Nickname")
                output_item["<b>Ссылка на продавца</b>"] = item.get("Seller Link")
            if setting[4] == 1:
                output_item["<b>Местоположение</b>"] = "Australia"
            if setting[5] == 1:
                output_item["<b>Описание товара</b>"] = item.get("Item Description")
            if setting[6] == 1:
                output_item["<b>Ссылка на изображение</b>"] = item.get("Item Picture")
            if setting[7] == 1:
                date_string = item.get("Date Created")
                date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S.%fZ')
                formatted_date = date_object.strftime('%d-%m-%Y %H:%M:%S')
                output_item["<b>Дата публикации</b>"] = formatted_date
            if setting[8] == 1:
                output_item["<b>Количество просмотров</b>"] = "Недоступно"
            if setting[9] == 1:
                output_item["<b>Дата регистрации</b>"] = "Недоступно"
            if setting[10] == 1:
                output_item["<b>Количество подписчиков продавца</b>"] = item.get("Seller Followers")
            if setting[11] == 1:
                output_item["<b>Дополнительная информация</b>"] = "Отсутствует"
            else:
                pass
        formatted_item = "\n".join([f"{key}: {value}" for key, value in output_item.items()])
        output_data.append(formatted_item)



    return output_data









