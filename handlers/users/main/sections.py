from aiogram import types

from keyboards.inline.inline_button import btns
from loader import dp


# Echo bot
@dp.message_handler(text="Бўлимлар")
async def bot_echo(message: types.Message):
    await message.answer("Танланг!", reply_markup=btns())
