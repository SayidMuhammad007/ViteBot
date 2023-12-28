from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
async def btns(request):
    btn = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for i in request:
        btn.insert(i)
    return btn

main_btn = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Бўлимлар"),
        KeyboardButton(text="Сўровнома ўтказиш")
    ],
    [
        KeyboardButton(text="Сўровномалар")
    ],
], resize_keyboard=True
)
competitionBtn = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Тугатиш")
    ],
[
        KeyboardButton(text="Асосий меню")
    ],
], resize_keyboard=True
)


cancel = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="❌ Бекор қилиш")
    ],
], resize_keyboard=True
)