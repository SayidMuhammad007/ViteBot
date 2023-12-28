from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.inline_button import ConfirmBtn
from loader import dp, db, bot
from secret import ADMINS
from states.sectionStates import adv


# Echo bot
@dp.message_handler(text="/users")
async def bot_echo(message: types.Message, state:FSMContext):
    if message.from_user.id in ADMINS:
        data = db.get_formatted_users_count()
        await message.answer(text=f"Jami foydalanuvchilar: {data}")

@dp.message_handler(text="/reklama")
async def bot_echo(message: types.Message, state:FSMContext):
    if message.from_user.id in ADMINS:
        await message.answer(text="Reklama xabarini yuboring!")
        await adv.content.set()

@dp.message_handler(state=adv.content)
async def bot_echo(message: types.Message, state:FSMContext):
    if message.from_user.id in ADMINS:
        await state.update_data({'content':message.text})
        await message.answer(text="Tasdiqlaysizmi?", reply_markup=ConfirmBtn())
        await adv.confirm.set()

@dp.callback_query_handler(state=adv.confirm)
async def bot_echo(callback: types.CallbackQuery, state:FSMContext):
    print(callback.message.from_user.id)
    if callback.from_user.id in ADMINS:
        if callback.data == "confirmYes":
            s = await state.get_data()
            msg = s.get("content")
            data = db.get_users()
            count = 0
            for i in data:
                count += 1
                # try:
                await bot.send_message(chat_id=i['tg_id'], text=msg)
                await callback.message.edit_text(f"Yuborildi: {count}")
                # except:
                #     pass
            await state.finish()