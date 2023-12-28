from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from handlers.users import subscription
from keyboards.default.button import main_btn
from keyboards.inline.inline_button import btns, user_vote
from loader import dp, db, bot
from secret import ADMINS, CHANNELS


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message, state:FSMContext):
    tg_id = message.from_user.id
    if tg_id in ADMINS:
        await message.answer(text=f"Assalomu alaykum {message.from_user.full_name}",reply_markup=main_btn)
    elif message.get_args():
        await state.update_data({'section_id' : message.get_args()})
        check = db.add_user(message.from_user.full_name, message.from_user.id, message.get_args())
        print("checccc", message.get_args())
        if check == 'error':
            await message.answer(text="Сиз аввал овоз бергансиз!")
        else:
            await state.update_data({'user_id':check})
            await checkSub(message, check)
#         await message.answer(f"""
# ❗️Илтимос, сўровномада иштирок этиш учун қуйидаги каналга аъзо бўлинг
# """)

async def checkSub(message, user_id):
    user = message.from_user.id
    final_status = True
    btn = InlineKeyboardMarkup(row_width=1)
    for channel in CHANNELS:
        status = await subscription.check(user_id=user,
                                          channel=channel)
        final_status *= status
        channel = await bot.get_chat(channel)
        if status:
            invite_link = await channel.export_invite_link()
            btn.add(InlineKeyboardButton(text=f"✅ {channel.title}", url=invite_link))
        if not status:
            invite_link = await channel.export_invite_link()
            btn.add(InlineKeyboardButton(text=f"❌ {channel.title}", url=invite_link))
    btn.add(InlineKeyboardButton(text="Обунани текшириш", callback_data="check_subs"))
    if final_status:
        await message.answer("Овоз беришингиз мумкин!", reply_markup=user_vote(message.get_args(), user_id))
    if not final_status:
        await message.answer("Ботдан фойдаланиш учун қуйидаги каналларга обуна бўлинг!",
                             disable_web_page_preview=True, reply_markup=btn)


@dp.callback_query_handler(text="check_subs")
async def checker(call: types.CallbackQuery, state:FSMContext):
    await call.answer()
    result = str()
    btn = InlineKeyboardMarkup()
    final_status = True
    for channel in CHANNELS:
        status = await subscription.check(user_id=call.from_user.id,
                                          channel=channel)
        final_status *=status
        channel = await bot.get_chat(channel)
        if not status:
            invite_link = await channel.export_invite_link()
            btn.add(InlineKeyboardButton(text=f"❌ {channel.title}", url=invite_link))

    btn.add(InlineKeyboardButton(text="Обунани текшириш", callback_data="check_subs"))
    if final_status:
        data = await state.get_data()
        arg = data.get("section_id")
        user_id = data.get("user_id")
        await call.message.edit_text("Овоз беришингиз мумкин!", reply_markup=user_vote(arg, user_id))
    if not final_status:
        await call.answer(cache_time=60)
        await call.message.answer("Сиз қуйидаги канал(лар)га обуна бўлмагансиз!",reply_markup=btn)
        await call.message.delete()
