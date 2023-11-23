from aiogram.fsm.state import StatesGroup, State


class Users(StatesGroup):
    user_id = State()