from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default.button import main_btn
from keyboards.inline.inline_button import btns, VoteBtn, btns_for_vote
from loader import dp, bot, db
from secret import CHANNEL_ID, CHANNELS
from states.sectionStates import new_competition


# Echo bot
@dp.message_handler(text="Сўровнома ўтказиш")
async def bot_echo(message: types.Message, state:FSMContext):
    await message.answer("Постни юборинг!")
    await new_competition.image.set()

@dp.message_handler(state=new_competition.image, content_types=types.ContentType.PHOTO)
async def bot_echo(message: types.Message, state:FSMContext):
    sent_message = await message.copy_to(chat_id="@" + CHANNEL_ID)
    image = f"https://t.me/{CHANNEL_ID}/{sent_message.message_id}"
    await state.update_data({'image' : image})
    await message.answer("Контентни ёзинг!")
    await new_competition.content.set()

@dp.message_handler(state=new_competition.content)
async def bot_echo(message: types.Message, state:FSMContext):
    await state.update_data({'content' : message.text})
    await message.answer("Бўлимни танланг!", reply_markup=btns_for_vote())
    await new_competition.part.set()


@dp.callback_query_handler(state=new_competition.part)
async def bot_echo(callback: types.CallbackQuery, state: FSMContext):
    connect_id = callback.data.split('_')[1]
    data = await state.get_data()
    content = data.get("content")

    msg = f"{content}\n\n<a href='https://t.me/rasmiy_sorovnoma_uz_bot?start={connect_id}'>Овоз бериш</a>"

    image = data.get("image")

    await callback.message.delete()

    print("msgg", msg)

    id = await bot.send_photo(
        chat_id=CHANNELS[0],
        photo=image,
        caption=msg,
        reply_markup=VoteBtn(connect_id)
    )
    db.add_competition(connect_id)
    db.add_msg(connect_id, id.message_id)

    await callback.message.answer("Танланг!", reply_markup=main_btn)

    await state.finish()