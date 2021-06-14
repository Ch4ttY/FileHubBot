import re

import asyncpg.exceptions
from aiogram import types, Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import CallbackQuery

from data.config import CHANNEL_LINK
from keyboards.inline.link_to_the_channel_keyboard import link_to_the_channel_keyboard, sponsor_link_keyboard, \
    check_subscription
from loader import dp, db_users, db_files, db_sponsors, bot
from utils.misc.subscription import check


@dp.message_handler(CommandStart(deep_link=re.compile(r"\d")))
async def bot_start_custom(message: types.Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        check_user = await db_users.check_user(user_id)

        if check_user != user_id:
            await db_users.add_user(
                full_name=message.from_user.full_name,
                username=message.from_user.username,
                telegram_id=message.from_user.id
            )

    except asyncpg.exceptions.UniqueViolationError:
        pass

    file_numb = int(message.get_args())

    if await db_files.check_file_exists(file_numb):
        file_id = await db_files.get_file_id(file_numb)
        sponsor_id = await db_sponsors.get_channel_link()
        chat = await bot.get_chat(sponsor_id)

        if chat.username is not None:
            sponsor_link = "t.me/" + chat.username
        else:
            sponsor_link = await chat.export_invite_link()

        await message.answer(text=f"Чтобы загрузить файл подпишитесь на канал спонсора:\n"
                                  f"{sponsor_link}",
                             reply_markup=sponsor_link_keyboard(sponsor_link),
                             disable_web_page_preview=True)

        await state.update_data(file_id=file_id)
        await state.update_data(sponsor_id=sponsor_id)
        await state.set_state("check_user_subscribe")

        await message.answer(text="Нажми на кнопку, чтобы загрузить файл 👇",
                             reply_markup=check_subscription)
    else:
        await message.answer(text=f"Такого файла не существует, чтобы скачать файл, перейди по ссылке под постом на канале {CHANNEL_LINK}",
                             reply_markup=link_to_the_channel_keyboard)


@dp.callback_query_handler(text="check_subscription", state="check_user_subscribe")
async def check_user_subscription(call: CallbackQuery, state: FSMContext):
    await call.answer()

    data = await state.get_data()

    file_id = data.get('file_id')
    sponsor_id = data.get("sponsor_id")
    user_id = call.from_user.id

    status = await check(user_id=user_id, channel=sponsor_id)

    if status:
        await call.message.answer_document(document=file_id,
                                           caption=f"Файл скачан в канале {CHANNEL_LINK}")
        await state.finish()
    else:
        channel = await bot.get_chat(sponsor_id)
        invite_link = await channel.export_invite_link()
        await call.message.answer(text=f"Подпишись на канал спонсора, чтобы скачать файл!\n\n {invite_link}",
                                  disable_web_page_preview=True)
        await state.finish()


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    try:
        user_id = message.from_user.id
        check_user = await db_users.check_user(user_id)

        if check_user != user_id:
            await db_users.add_user(
                full_name=message.from_user.full_name,
                username=message.from_user.username,
                telegram_id=message.from_user.id
            )

    except asyncpg.exceptions.UniqueViolationError:
        pass

    await message.answer(text=f"❌ {message.from_user.full_name}, задайте файл для скачивания!!!\n\n"
                         f"Чтобы скачать необходимый файл, необходимо перейти по ссылке на него в канале {CHANNEL_LINK}",
                         reply_markup=link_to_the_channel_keyboard,
                         disable_web_page_preview=True)

