import asyncpg
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, AdminFilter
from aiogram.types import CallbackQuery

from data.config import ADMINS, CHANNEL_LINK
from filters.forwarded_message import IsForwarded
from keyboards.inline.admin_main_keyboard import admin_main_keyboard, file_loading_keyboard, sponsor_loading_keyboard
from loader import dp, db_files, bot, db_sponsors


@dp.callback_query_handler(text="load_file", user_id=ADMINS)
async def load_file(call: CallbackQuery):
    await call.answer()

    await call.message.edit_text(text="Отправь файл, который хочешь загрузить или обновить",
                                 reply_markup=file_loading_keyboard)


# @dp.callback_query_handler(text="admin", user_id=ADMINS, state="*")
@dp.callback_query_handler(text="admin",  state="*")
async def back_to_admin_menu(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_text(text="Управление хранилищем",
                                 reply_markup=admin_main_keyboard)


# @dp.message_handler(Command("admin"), user_id=ADMINS, state="*")
@dp.message_handler(Command("admin"), state="*")
async def admin_command(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(text="Управление хранилищем",
                         reply_markup=admin_main_keyboard)


@dp.message_handler(content_types=types.ContentTypes.DOCUMENT)
async def get_file(message: types.Message):
    file_id = message.document.file_id

    await db_files.add_file(file_id)

    get_file_numb = await db_files.get_file_numb(file_id)
    bot_info = await bot.me

    link_to_the_file = f"t.me/{bot_info.username}?start={get_file_numb}"

    await message.answer(text=f"Файл сохранён\n\n"
                              f"Ссылка на файл: {link_to_the_file}",
                         disable_web_page_preview=True)


# @dp.callback_query_handler(user_id=ADMINS, text="sponsor_channel_link")
@dp.callback_query_handler(text="sponsor_channel_link")
async def sponsor_channel_link_add(call: CallbackQuery, state: FSMContext):
    await call.answer()

    await call.message.edit_text(text="Перешли в бота любое сообщение из канал спонсора",
                                 reply_markup=sponsor_loading_keyboard,
                                 disable_web_page_preview=True)
    await state.set_state("adding_sponsor_link")


# @dp.message_handler(IsForwarded(), content_types=types.ContentTypes.ANY, user_id=ADMINS, state="adding_sponsor_link")
@dp.message_handler(IsForwarded(), content_types=types.ContentTypes.ANY,state="adding_sponsor_link")
async def getting_sponsor_link(message: types.Message, state: FSMContext):
    sponsor_id = str(message.forward_from_chat.id)

    await db_sponsors.add_sponsor(sponsor_id)

    await message.answer("Канал спонсора обновлен")
    await state.finish()