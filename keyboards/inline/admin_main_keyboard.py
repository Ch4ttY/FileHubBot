from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

admin_main_keyboard = InlineKeyboardMarkup(row_width=1,
                                            inline_keyboard=[
                                                [
                                                    InlineKeyboardButton(
                                                        text="🗂 Загрузить файл",
                                                        callback_data="load_file"

                                                    ),
                                                ],
                                                [
                                                    InlineKeyboardButton(
                                                        text="💰 Канал спонсора",
                                                        callback_data="sponsor_channel_link"

                                                    ),
                                                ],
                                                [
                                                    InlineKeyboardButton(
                                                        text="📩 Рассылка",
                                                        callback_data="broadcast"

                                                    ),
                                                ]
                                            ])

file_loading_keyboard = InlineKeyboardMarkup(row_width=1,
                                            inline_keyboard=[
                                                [
                                                    InlineKeyboardButton(
                                                        text="❌ Отмена",
                                                        callback_data="admin"

                                                    ),
                                                ]
                                            ])


sponsor_loading_keyboard = InlineKeyboardMarkup(row_width=1,
                                            inline_keyboard=[
                                                [
                                                    InlineKeyboardButton(
                                                        text="❌ Отмена",
                                                        callback_data="admin"

                                                    ),
                                                ]
                                            ])

broadcast_loading_keyboard = InlineKeyboardMarkup(row_width=1,
                                            inline_keyboard=[
                                                [
                                                    InlineKeyboardButton(
                                                        text="❌ Отмена",
                                                        callback_data="admin"

                                                    ),
                                                ]
                                            ])