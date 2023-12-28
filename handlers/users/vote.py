from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.inline_button import VoteBtn
from loader import dp, db, bot
from secret import CHANNELS


# Echo bot
@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('voteTo_'))
async def handle_product_deletion(callback_query: types.CallbackQuery, state: FSMContext):
    part_id = callback_query.data.split('_')[1]
    user_id = callback_query.data.split('_')[2]
    section_id = callback_query.data.split('_')[3]
    db.addVote(user_id, part_id, section_id)
    data = db.get_msg(section_id)
    message_id = data[0]['msg_id']
    print("mssid", message_id)
    await bot.edit_message_reply_markup(
        chat_id=CHANNELS[0],
        message_id=message_id,
        reply_markup=VoteBtn(section_id)
    )
    await callback_query.message.edit_text("Овозингиз қабул қилинди!")
