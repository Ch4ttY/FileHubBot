from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from aiogram_broadcaster import MessageBroadcaster


from data.config import ADMINS
from keyboards.inline.admin_main_keyboard import broadcast_loading_keyboard
from loader import dp, db_users


# @dp.callback_query_handler(user_id=ADMINS, text='broadcast')
@dp.callback_query_handler(text='broadcast')
async def broadcast_command_handler(call: CallbackQuery, state: FSMContext):
    await call.answer()

    await call.message.edit_text('Введите текст для начала рассылки:',
                              reply_markup=broadcast_loading_keyboard)
    await state.set_state('broadcast_text')


@dp.message_handler(state='broadcast_text', content_types=types.ContentTypes.ANY)
async def start_broadcast(msg: Message, state: FSMContext):
    await state.finish()

    users = await db_users.select_all_users()
    await MessageBroadcaster(users, msg).run()
