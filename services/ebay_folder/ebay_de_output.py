from datetime import datetime
import json
from app import database as db


async def output_ebay_de(user_id):
    user_settings = await db.check_user_settings(user_id)

    with open('services/ebay_folder/ebay_de_output.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    output_data = []
    for item in data:
        output_item = {}  # Создаем новый словарь для каждого товара в JSON
        for setting in user_settings:
            if setting[1] == 1:
                output_item["<b>Название товара</b>"] = item.get("Name")
                output_item["<b>Ссылка на товар</b>"] = item.get("Item Link")
            if setting[2] == 1:
                output_item["<b>Цена товара</b>"] = item.get("Price")
            if setting[3] == 1:
                output_item["<b>Имя продавца</b>"] = item.get("Seller Nickname")
                output_item["<b>Ссылка на продавца</b>"] = item.get("Seller Link")
            if setting[4] == 1:
                output_item["<b>Местоположение</b>"] = "Germany"
            if setting[5] == 1:
                output_item["<b>Состояние товара</b>"] = item.get("Item Condition")
            if setting[6] == 1:
                output_item["<b>Ссылка на изображение</b>"] = item.get("Item Picture")
            if setting[7] == 1:
                output_item["<b>Дата публикации</b>"] = "Отсутствует на сайте"
            if setting[8] == 1:
                output_item["<b>Количество просмотров</b>"] = "Недоступно"
            if setting[9] == 1:
                output_item["<b>Дата регистрации</b>"] = "Недоступно"
            if setting[10] == 1:
                output_item["<b>Фидбек продавца</b>"] = item.get("Seller Feedback")
            if setting[11] == 1:
                output_item["<b>Количество проданных товаров продавца</b>"] = item.get("Seller Sold Items")
            else:
                pass
        formatted_item = "\n".join([f"{key}: {value}" for key, value in output_item.items()])
        output_data.append(formatted_item)


    return output_data