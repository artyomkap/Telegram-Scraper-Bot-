from aiogram.fsm.state import StatesGroup, State



class ParserOutput(StatesGroup):
    item_name = State()
    item_price = State()
    item_seller = State()
    item_location = State()
    item_description = State()
    item_picture = State()
    item_publish_date = State()
    item_views = State()
    seller_registration_date = State()
    seller_items_number = State()
    item_extra_info = State()
    output_files = State()
