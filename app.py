import logging

from aiogram import executor

from loader import dp, db_users, db_files, db_sponsors
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)

    logging.info("Создаем подключение к базе данных")

    await db_users.create()
    logging.info("Создаем таблицу пользователей")
    await db_users.create_table_users()

    await db_files.create()
    logging.info("Создаем таблицу файлов")
    await db_files.create_table_files()


    await db_sponsors.create()
    logging.info("Создаем таблицу файлов")
    await db_sponsors.create_table_sponsors()


    logging.info("Готово")

    # Уведомляет про запуск
    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
