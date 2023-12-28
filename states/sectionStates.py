from aiogram.dispatcher.filters.state import State, StatesGroup

class new_section(StatesGroup):
    name = State()

class new_part(StatesGroup):
    name = State()

class new_competition(StatesGroup):
    image = State()
    content = State()
    part = State()

class adv(StatesGroup):
    content = State()
    confirm = State()