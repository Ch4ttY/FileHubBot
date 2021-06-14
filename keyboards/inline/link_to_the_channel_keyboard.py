from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data.config import CHANNEL_LINK

link_to_the_channel_keyboard = InlineKeyboardMarkup(row_width=1,
                                                    inline_keyboard=[
                                                        [
                                                            InlineKeyboardButton(
                                                                text="Перейти на канал",
                                                                url=CHANNEL_LINK

                                                            ),
                                                        ]
                                                    ])


def sponsor_link_keyboard(sponsor_link):
    sponsor_link_keyboard = InlineKeyboardMarkup(row_width=1,
                                                inline_keyboard=[
                                                    [
                                                        InlineKeyboardButton(
                                                            text="👉 Подписаться",
                                                            url=sponsor_link
                                                        )
                                                    ]
                                                ])
    return sponsor_link_keyboard


check_subscription = InlineKeyboardMarkup(row_width=1,
                                            inline_keyboard=[
                                                [
                                                    InlineKeyboardButton(
                                                        text="✅ Я подписался",
                                                        callback_data="check_subscription"
                                                    )
                                                ]
                                            ])
