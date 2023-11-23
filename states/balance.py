from aiogram.fsm.state import StatesGroup, State



class Balance(StatesGroup):
    amount = State()