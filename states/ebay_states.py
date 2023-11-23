from aiogram.fsm.state import StatesGroup, State



class Ebay(StatesGroup):
    search = State()
    category = State()
    priceMax = State()
    priceMin = State()
    sort = State()
    quantity = State()

