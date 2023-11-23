import datetime
import sqlite3 as sq
import time

db = sq.connect('TGParser.db')
cur = db.cursor()


async def db_start():
    cur.execute("CREATE TABLE IF NOT EXISTS users("
                "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                "user_id INTEGER,"
                "sub_time INTEGER,"
                "balance INTEGER,"
                "message_id INTEGER)")
    db.commit()


async def cmd_start_db(user_id):
    user = cur.execute("SELECT * FROM users WHERE user_id == {key}".format(key=user_id)).fetchone()
    if not user:
        cur.execute("INSERT INTO users (user_id, status) VALUES (?, ?)", (user_id, "active")).fetchall()
        cur.execute("UPDATE `users` SET `balance` = ? WHERE `user_id` = ?", (2.0, user_id,))
        db.commit()


async def get_user_info(user_id):
    user = cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchall()
    if user:
        user_info = user
        return user_info
    else:
        return None


async def get_user_status(user_id):
    status = cur.execute("SELECT status FROM users WHERE user_id = ?", (user_id,)).fetchall()
    if status:
        for status in status:
            normal_status = status[0]
            return normal_status


async def block_user(user_id):
    cur.execute('UPDATE users SET status = "blocked" WHERE user_id = ?', (user_id,)).fetchall()
    db.commit()


async def unblock_user(user_id):
    cur.execute('UPDATE users SET status = "active" WHERE user_id = ?', (user_id,)).fetchall()
    db.commit()


async def select_all_users():
    users = cur.execute("SELECT user_id FROM users").fetchall()
    if users:
        return users


async def cmd_start_user_settings(user_id):
    user = cur.execute('SELECT * FROM user_settings WHERE user_id == ?', (user_id,)).fetchall()
    if not user:
        cur.execute(
            "INSERT INTO user_settings (user_id, item_name, item_price, item_seller, item_location, item_description, item_picture, item_publish_date, item_views, seller_registration_date, seller_items_number, item_extra_info, output_files) VALUES (?, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)",
            (user_id,)).fetchall()
        db.commit()


async def get_balance(user_id):
    result = cur.execute("SELECT `balance` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
    if result:
        for row in result:
            if row[0] is not None:
                balance = float(row[0])
                return balance
            else:
                return 0


async def change_balance(user_id, amount: float, balance: float):
    new_amount = float(amount)
    new_balance = balance + new_amount
    result = cur.execute("UPDATE `users` SET `balance` = ? WHERE `user_id` = ?", (new_balance, user_id)).fetchall()
    db.commit()


async def check_balance(user_id, amount: float):
    result = cur.execute("SELECT `balance` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
    if result:
        for row in result:
            if row[0] is not None:
                balance = float(row[0])
                await change_balance(user_id, amount, balance)
            else:
                return False


async def give_time_sub_1day(user_id):
    time_now = int(time.time())
    time_sub = time_now + (24 * 60 * 60)
    sub_price = await get_subscriptions_price()
    if sub_price:
        cur.execute("UPDATE `users` SET `sub_time` = ? WHERE `user_id` = ?", (time_sub, user_id,))
        db.commit()


async def give_time_sub_3days(user_id):
    time_now = int(time.time())
    time_sub = time_now + (72 * 60 * 60)
    sub_price = await get_subscriptions_price()
    if sub_price:
        cur.execute("UPDATE `users` SET `sub_time` = ? WHERE `user_id` = ?", (time_sub, user_id,))
        db.commit()


async def give_time_sub_1week(user_id):
    time_now = int(time.time())
    time_sub = time_now + (7 * 24 * 60 * 60)
    sub_price = await get_subscriptions_price()
    if sub_price:
        cur.execute("UPDATE `users` SET `sub_time` = ? WHERE `user_id` = ?", (time_sub, user_id,))
        db.commit()


async def give_time_sub_1month(user_id):
    time_now = int(time.time())
    time_sub = time_now + (30 * 24 * 60 * 60)
    sub_price = await get_subscriptions_price()
    if sub_price:
        cur.execute("UPDATE `users` SET `sub_time` = ? WHERE `user_id` = ?", (time_sub, user_id,))
        db.commit()


async def set_time_sub_1day(user_id):
    time_now = int(time.time())
    time_sub = time_now + (24 * 60 * 60)
    result = cur.execute("SELECT `balance` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
    sub_price = await get_subscriptions_price()
    if sub_price:
        sub_1day_price = sub_price[0]
        if result and sub_price:
            for row in result:
                if row[0] is not None:
                    balance = int(row[0])
                    if balance is not None and balance < sub_1day_price:
                        return False
                    else:
                        new_balance = balance - sub_1day_price
                        cur.execute("UPDATE `users` SET `balance` = ? WHERE `user_id` = ?",
                                    (new_balance, user_id)).fetchall()
                        db.commit()
                        cur.execute("UPDATE `users` SET `sub_time` = ? WHERE `user_id` = ?", (time_sub, user_id,))
                        db.commit()
                        return True


async def set_time_sub_3days(user_id):
    time_now = int(time.time())
    time_sub = time_now + (72 * 60 * 60)
    result = cur.execute("SELECT `balance` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
    sub_price = await get_subscriptions_price()
    if sub_price:
        sub_3day_price = sub_price[1]
    if result:
        for row in result:
            if row[0] is not None:
                balance = int(row[0])
                if balance is not None and balance < sub_3day_price:
                    return False
                else:
                    new_balance = balance - sub_3day_price
                    cur.execute("UPDATE `users` SET `balance` = ? WHERE `user_id` = ?",
                                (new_balance, user_id)).fetchall()
                    db.commit()
                    cur.execute("UPDATE `users` SET `sub_time` = ? WHERE `user_id` = ?", (time_sub, user_id,))
                    db.commit()
                    return True


async def set_time_sub_1week(user_id):
    time_now = int(time.time())
    time_sub = time_now + (7 * 24 * 60 * 60)
    result = cur.execute("SELECT `balance` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
    sub_price = await get_subscriptions_price()
    if sub_price:
        sub_1week_price = sub_price[2]
    if result:
        for row in result:
            if row[0] is not None:
                balance = int(row[0])
                if balance is not None and balance < sub_1week_price:
                    return False
                else:
                    new_balance = balance - sub_1week_price
                    cur.execute("UPDATE `users` SET `balance` = ? WHERE `user_id` = ?",
                                (new_balance, user_id)).fetchall()
                    db.commit()
                    cur.execute("UPDATE `users` SET `sub_time` = ? WHERE `user_id` = ?", (time_sub, user_id,))
                    db.commit()
                    return True


async def set_time_sub_1month(user_id):
    time_now = int(time.time())
    time_sub = time_now + (30 * 24 * 60 * 60)
    result = cur.execute("SELECT `balance` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
    sub_price_1 = await get_subscriptions_price()
    if sub_price_1:
        sub_1month_price = sub_price_1[3]
    if result:
        for row in result:
            if row[0] is not None:
                balance = int(row[0])
                if balance is not None and balance < sub_1month_price:
                    return False
                else:
                    new_balance = balance - sub_1month_price
                    cur.execute("UPDATE `users` SET `balance` = ? WHERE `user_id` = ?",
                                (new_balance, user_id)).fetchall()
                    db.commit()
                    cur.execute("UPDATE `users` SET `sub_time` = ? WHERE `user_id` = ?", (time_sub, user_id,))
                    db.commit()
                    return True


async def get_subscriptions_price():
    result = cur.execute('SELECT `price` FROM `subscriptions`').fetchall()
    if result:
        prices = [int(row[0]) for row in result if row[0] is not None]
        return prices


async def get_subscription_time():
    result = cur.execute('SELECT `length` FROM `subscriptions`').fetchall()
    if result:
        length = [str(row[0]) for row in result if row[0] is not None]
        return length


async def change_subscription_price(new_price, length):
    cur.execute('UPDATE `subscriptions` SET `price` = ? WHERE `length` = ?', (new_price, length,))
    db.commit()


async def get_time_sub(user_id):
    result = cur.execute("SELECT `sub_time` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
    if result:
        for row in result:
            if row[0] is not None:
                time_sub = int(row[0])
                return time_sub
            else:
                return 0


async def get_sub_status(user_id):
    time_sub = 0
    result = cur.execute("SELECT `sub_time` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
    if result:
        for row in result:
            if row[0] is not None:
                time_sub = int(row[0])
        if time_sub > int(time.time()):
            return True
    return False


async def check_user_settings(user_id):
    result = cur.execute("SELECT * FROM `user_settings` WHERE `user_id` = ?", (user_id,)).fetchall()
    if result:
        return result


async def check_user_settings_kb(user_id):
    result = cur.execute("SELECT * FROM `user_settings` WHERE `user_id` = ?", (user_id,)).fetchone()
    if result:
        columns = [desc[0] for desc in cur.description]  # Получаем названия столбцов
        settings_data = dict(zip(columns, result))  # Создаем словарь с названиями столбцов в качестве ключей
        return settings_data
    else:
        return None


async def turn_off_user_setting(user_id, setting):
    setting = setting
    cur.execute(f"UPDATE user_settings SET {setting} = 0 WHERE user_id = ?", (user_id,))
    db.commit()


async def turn_on_user_setting(user_id, setting):
    setting = setting
    cur.execute(f"UPDATE user_settings SET {setting} = 1 WHERE user_id = ?", (user_id,))
    db.commit()


async def update_message_id(user_id, message_id):
    cur.execute("UPDATE users SET message_id = ? WHERE user_id = ?", (message_id, user_id,)).fetchall()
    db.commit()


async def get_message_id(user_id):
    result = cur.execute("SELECT message_id FROM users WHERE user_id = ?", (user_id,)).fetchall()
    if result:
        return result


async def add_payment_crypto_bot(payment_id: int, amount: float):
    if payment_id is not None and amount is not None:
        cur.execute("INSERT INTO payments (payment_id, sum) VALUES (?, ?)", (payment_id, amount)).fetchall()
        db.commit()


async def get_payment_crypto_bot(payment_id: int):
    result = cur.execute("SELECT * FROM payments WHERE payment_id = ?", (payment_id,)).fetchall()
    if result:
        return result


async def delete_payment_crypto_bot(payment_id: int):
    cur.execute("DELETE FROM payments WHERE payment_id = ?", (payment_id,)).fetchall()
    db.commit()


async def klein_save_preset(user_id, preset_name, category, search, priceMax, priceMin, sort):
    cur.execute("INSERT INTO user_presets VALUES (?, ?, ?, ?, ?, ?, ?)",
                (user_id, preset_name, category, search, priceMax, priceMin, sort,)).fetchall()
    db.commit()


async def get_klein_preset(user_id):
    result = cur.execute("SELECT * FROM user_presets WHERE user_id = ?", (user_id,)).fetchall()
    if result:
        return result


async def get_klein_preset_by_name(user_id, preset_name):
    result = cur.execute("SELECT * FROM user_presets WHERE user_id = ? AND preset_name = ?",
                         (user_id, preset_name)).fetchall()
    if result:
        return result


async def delete_klein_preset(user_id, preset_name):
    cur.execute("DELETE FROM user_presets WHERE user_id = ? AND preset_name = ?", (user_id, preset_name)).fetchall()
    db.commit()


async def get_klein_parsings(user_id, url):
    result = cur.execute("SELECT * FROM klein_parsings WHERE user_id = ? AND url = ?", (user_id, url)).fetchall()
    if result:
        return result
    elif result is None:
        return "not found"


async def add_klein_parsings(user_id, url):
    time_now = int(time.time())
    cur.execute("INSERT INTO klein_parsings (user_id, url, parse_num, time_parse) VALUES (?, ?, ?, ?)", (user_id, url, 1, time_now)).fetchall()
    db.commit()


async def update_klein_parsings(user_id, url):
    new_parse_num = None
    result = cur.execute("SELECT * FROM klein_parsings WHERE user_id = ? AND url = ?", (user_id, url)).fetchall()
    if result:
        for res in result:
            parse_num = res[2]
            new_parse_num = parse_num + 1
        cur.execute("UPDATE klein_parsings SET parse_num = ? WHERE user_id = ? AND url = ?",
                    (new_parse_num, user_id, url)).fetchall()
        db.commit()


async def delete_klein_parsings(user_id, url):
    cur.execute("DELETE FROM klein_parsings WHERE user_id = ? AND url = ?", (user_id, url)).fetchall()
    db.commit()
