from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default.button import cancel, main_btn
from keyboards.inline.inline_button import btns, delete
from loader import dp, db
from states.sectionStates import new_section


@dp.message_handler(lambda message: message.text in ["/start", "❌ Бекор қилиш"], state="*")
async def start_command(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(text=f"Танланг!", reply_markup=main_btn)

# Echo bot
@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('delete_section'))
async def handle_product_deletion(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.edit_text(text="Танланг", reply_markup=delete())


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('delete_'))
async def handle_product_deletion(callback_query: types.CallbackQuery, state: FSMContext):
    connect_id = callback_query.data.split('_')[1]
    db.delete(connect_id)
    await callback_query.message.delete()
    await callback_query.message.answer("Танланг!", reply_markup=main_btn)