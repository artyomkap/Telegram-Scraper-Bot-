from aiogram.fsm.state import StatesGroup, State

class Subscription(StatesGroup):
    price = State()
    length = State()
