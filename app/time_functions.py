import time
import datetime


def days_to_seconds(days):
    return days * 24 * 60 * 60

def format_timedelta(td):
    seconds = td.seconds
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    if td.days <= 0 and hours <= 0 and minutes <= 0 and seconds <= 0:
        return "Подписка истекла!"

    minutes_str = "минут" if minutes != 1 else "минута"
    seconds_str = "секунд" if seconds != 1 else "секунда"

    if hours == 1 or hours == 21:
        hours_str = "час"
    elif 2 <= hours <= 4 or 22 <= hours <= 23:
        hours_str = "часа"
    else:
        hours_str = "часов"

    days = td.days
    if days == 1:
        days_str = "день"
    elif 1 < days < 5:
        days_str = "дня"
    else:
        days_str = "дней"

    return f"{days} {days_str}, {hours} {hours_str}, {minutes} {minutes_str}, {seconds} {seconds_str}"

def time_sub_day(get_time):
    time_now = int(time.time())
    middle_time = int(get_time) - time_now

    if middle_time <= 0:
        return datetime.timedelta(seconds=0)
    else:
        return datetime.timedelta(seconds=middle_time)
