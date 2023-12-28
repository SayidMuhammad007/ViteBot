from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default.button import cancel, main_btn
from keyboards.inline.inline_button import btns
from loader import dp, db
from states.sectionStates import new_section


@dp.message_handler(lambda message: message.text in ["/start", "❌ Бекор қилиш", 'Асосий меню'], state="*")
async def start_command(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(text=f"Танланг!", reply_markup=main_btn)

# Echo bot
@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('new_section'))
async def handle_product_deletion(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.edit_text(text="Бўлим номи")
    await new_section.name.set()

@dp.message_handler(state=new_section.name)
async def handle_product_deletion(message: types.Message, state: FSMContext):
    db.add_section(message.text)
    await message.answer(text="Сақланди")
    await message.answer(text="Бўлим номи", reply_markup=cancel)
    await new_section.name.set()