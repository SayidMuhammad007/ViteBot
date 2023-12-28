from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import exceptions

from loader import db, dp, bot

page_number = 1
page_size = 5
connect_id = None

@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('section_'))
async def handle_product_deletion(callback_query: types.CallbackQuery, state: FSMContext):
    global page_number
    global page_size
    global connect_id
    connect_id = callback_query.data.split('_')[1]
    await state.update_data({'section': connect_id})
    page_number = 1
    data = db.get_paginated_data(page_number, page_size, connect_id)
    text, markup = generate_message_text(data)

    try:
        await callback_query.message.edit_text(text=text, reply_markup=markup)
    except exceptions.MessageTextIsEmpty:
        pass

@dp.callback_query_handler(lambda c: c.data in ['prev2', 'next2'])
async def process_callback(callback_query: types.CallbackQuery):
    global page_number
    global page_size

    action = callback_query.data
    if action == 'prev2':
        page_number = max(1, page_number - 1)
    elif action == 'next2':
        page_number += 1

    data = db.get_paginated_data(page_number, page_size, connect_id)
    text, markup = generate_message_text(data)

    await callback_query.message.edit_text(text=text, reply_markup=markup)

def generate_message_text(data):
    global page_size
    global page_number

    has_previous_page = page_number > 1
    has_next_page = len(data) > page_size * (page_number - 1)

    markup = InlineKeyboardMarkup()
    keyboard = []

    for user_instance, in data:
        button = InlineKeyboardButton(
            text=f"{user_instance.name}",
            callback_data=f"part_{user_instance.id}"
        )
        keyboard.append([button])

    markup.inline_keyboard = keyboard

    if has_previous_page:
        markup.row(InlineKeyboardButton("⬅️ Олдингилари", callback_data="prev2"))

    if has_next_page:
        if has_previous_page:
            markup.insert(InlineKeyboardButton("Кейингилари ➡️", callback_data="next2"))
        else:
            markup.add(InlineKeyboardButton("Кейингилари ➡️", callback_data="next2"))
    markup.add(InlineKeyboardButton("➕ Янги қўшиш", callback_data="new_part"))
    return "Танланг!", markup