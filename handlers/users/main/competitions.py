from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default.button import competitionBtn, main_btn
from keyboards.inline.inline_button import btns, votes
from loader import dp, db


# Echo bot
@dp.message_handler(text="Сўровномалар")
async def bot_echo(message: types.Message):
    await message.answer("Танланг!", reply_markup=votes())

@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('competition_'))
async def handle_product_deletion(callback_query: types.CallbackQuery, state: FSMContext):
    connect_id = callback_query.data.split('_')[1]
    data = db.Statistic(connect_id)
    msg = ""
    for i in data:
        msg += f"""
{i['name']} : {i['votes_count']} ta ovoz
"""
    await state.update_data({'connect_id':connect_id})
    await callback_query.message.delete()
    await callback_query.message.answer(text=msg, reply_markup=competitionBtn)

@dp.message_handler(text="Тугатиш")
async def bot_echo(message: types.Message, state:FSMContext):
    data = await state.get_data()
    id = data.get("connect_id")
    result = db.finish(id)
    msg = """
Овоз бериш якунланди!
Натижалар
    """
    for i in result:
        msg += f"""
{i['name']} : {i['votes_count']} ta ovoz
    """
    await message.answer(text=msg, reply_markup=main_btn)
