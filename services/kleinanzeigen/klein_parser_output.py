import os
import threading
from datetime import datetime
import json
import aiofiles
import fasteners

from app import database as db




async def klein_number_of_items():
    file_path = 'services/kleinanzeigen/klein_output.json'

    if os.path.exists(file_path):
        async with aiofiles.open(file_path, 'r', encoding='utf-8') as json_file:
            data = await json_file.read()

            # Проверка наличия данных
            if not data:
                return "Попробуйте обновить еще раз"

            json_data = json.loads(data)
            collected_items = len(json_data)
            return collected_items
    else:
        return 0



async def delete_items_with_rating():
    async with aiofiles.open('services/kleinanzeigen/klein_output.json', 'r', encoding='utf-8') as json_file:
        data = await json_file.read()
        items = json.loads(data)

    # Фильтрация элементов по условию
    filtered_items = [item for item in items if item.get("Seller Feedback") not in "Zufriedenheit: TOP"]

    # Запись обновленных данных обратно в JSON файл
    async with aiofiles.open('services/kleinanzeigen/klein_output.json', 'w', encoding='utf-8') as json_file:
        await json_file.write(json.dumps(filtered_items, indent=4, ensure_ascii=False))



async def delete_items_without_shipping():
    file_path = 'services/kleinanzeigen/klein_output.json'

    # Чтение данных из файла
    async with aiofiles.open(file_path, 'r', encoding='utf-8') as json_file:
        data = await json_file.read()

    # Загрузка JSON данных
    items = json.loads(data)

    # Фильтрация элементов по условию
    filtered_items = [item for item in items if item.get("Item Shipping", "").lower() != "доставки нет"]

    # Запись обновленных данных обратно в JSON файл
    async with aiofiles.open(file_path, 'w', encoding='utf-8') as json_file:
        await json_file.write(json.dumps(filtered_items, indent=4, ensure_ascii=False))


async def sort_items_by_registration_date():
    async with aiofiles.open('services/kleinanzeigen/klein_output.json', 'r', encoding='utf-8') as json_file:
        data = await json_file.read()
        items = json.loads(data)

    def get_registration_date(item):
        date_str = item.get("Seller Registration Date", "Aktiv seit 01.01.1970")
        date_obj = datetime.strptime(date_str, "Aktiv seit %d.%m.%Y")
        return date_obj

    sorted_data = sorted(items, key=get_registration_date, reverse=True)

    async with aiofiles.open('services/kleinanzeigen/klein_output.json', 'w', encoding='utf-8') as json_file:
        await json_file.write(json.dumps(sorted_data, ensure_ascii=False, indent=4))



async def get_registration_date(item):
    registration_date = item.get("Seller Registration Date", "01.01.1970")
    # Разбиваем дату по точкам и преобразуем в формат даты
    parts = registration_date.split(".")
    return int(parts[2]), int(parts[1]), int(parts[0])


async def sort_items():
    registration_dates = []
    with open('services/kleinanzeigen/klein_output.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    for item in data:
        registration_dates.append((item, await get_registration_date(item)))
    # Сортируем товары по дате регистрации в обратном порядке (от новых к старым)
    sorted_items = [item for item, _ in sorted(registration_dates, key=lambda x: x[1], reverse=True)]
    return sorted_items



async def output_klein(user_id):
    user_settings = await db.check_user_settings(user_id)

    with open('services/kleinanzeigen/klein_output.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    output_data = []
    for item in data:
        output_item = {}
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
                output_item["<b>Описание товара</b>"] = item.get("Item Description")
            if setting[6] == 1:
                output_item["<b>Ссылка на изображение</b>"] = item.get("Item Picture")
            if setting[7] == 1:
                output_item["<b>Дата публикации</b>"] = item.get("Item Publish Date")
            if setting[8] == 1:
                output_item["<b>Возможность доставки</b>"] = item.get("Item Shipping")
            if setting[9] == 1:
                output_item["<b>Дата регистрации</b>"] = item.get("Seller Registration Date")
            if setting[10] == 1:
                output_item["<b>Количество товаров продавца</b>"] = item.get("Seller Items")
            if setting[11] == 1:
                output_item["<b>Фидбек продавца</b>"] = item.get("Seller Feedback")
            else:
                pass
        formatted_item = "\n".join([f"{key}: {value}" for key, value in output_item.items()])
        output_data.append(formatted_item)



    return output_data