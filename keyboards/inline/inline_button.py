from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import db
from secret import LINK


def btns():
    request = db.selectAll()
    keyboard = InlineKeyboardMarkup(row_width=2)
    for row in request:
        button = InlineKeyboardButton(row['name'], callback_data=f"section_{row['id']}")
        keyboard.insert(button)

    new_section_button = InlineKeyboardButton("Янги қўшиш", callback_data="new_section")
    keyboard.add(new_section_button)
    new_section_button = InlineKeyboardButton("❌ Ўчириш", callback_data="delete_section")
    keyboard.insert(new_section_button)
    return keyboard

def delete():
    request = db.selectAll()
    keyboard = InlineKeyboardMarkup(row_width=2)
    for row in request:
        button = InlineKeyboardButton(row['name'], callback_data=f"delete_{row['id']}")
        keyboard.insert(button)
    return keyboard

def user_vote(id, user_id):
    request = db.selectAllForUser(id)
    keyboard = InlineKeyboardMarkup(row_width=2)
    print(request)
    for row in request:
        button = InlineKeyboardButton(row['name'], callback_data=f"voteTo_{row['id']}_{user_id}_{id}")
        keyboard.insert(button)


    return keyboard

def votes():
    request = db.SelectAllComp()
    keyboard = InlineKeyboardMarkup(row_width=2)
    for row in request:
        button = InlineKeyboardButton(row['name'], callback_data=f"competition_{row['id']}")
        keyboard.insert(button)


    return keyboard

def VoteBtn(data):
    request = db.selectAllForUser(data)
    keyboard = InlineKeyboardMarkup(row_width=2)
    for row in request:
        button = InlineKeyboardButton(f"{row['name']} - {row['votes_count']}", url=f"{LINK}{data}")
        keyboard.add(button)

    return keyboard

def btns_for_vote():
    request = db.selectForVote()
    keyboard = InlineKeyboardMarkup(row_width=2)
    print(request)
    for row in request:
        print("rowww")
        button = InlineKeyboardButton(row['name'], callback_data=f"section_{row['id']}")
        keyboard.insert(button)

    return keyboard

def ConfirmBtn():
    btn = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Tasdiqlash", callback_data="confirmYes"),
            InlineKeyboardButton(text="❌ Bekor qilish", callback_data="confirmNo"),
        ]
    ])
    return btn