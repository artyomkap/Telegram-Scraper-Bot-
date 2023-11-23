from aiogram.fsm.state import StatesGroup, State


class Klein(StatesGroup):
    url = State()
    search = State()
    category = State()
    priceMax = State()
    priceMin = State()
    sort = State()
    quantity = State()

