from aiogram.fsm.state import StatesGroup, State


class KleinState(StatesGroup):
    name = State()
    quantity = State()