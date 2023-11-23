from aiogram.fsm.state import StatesGroup, State


class KleinUrl(StatesGroup):
    url = State()
    quantity = State()