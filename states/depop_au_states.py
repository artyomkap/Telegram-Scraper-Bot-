from aiogram.fsm.state import StatesGroup, State



class DepopAu(StatesGroup):
    search = State()
    priceMax = State()
    priceMin = State()
    sort = State()
    quantity = State()
    country = State()
