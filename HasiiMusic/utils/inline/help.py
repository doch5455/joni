from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from HasiiMusic import app


def help_keyboard(_):
    buttons = []
    # 🔹 Sadece 4 başlık gösterilir (H_B_1 - H_B_4)
    for i in range(1, 5):
        if (i - 1) % 2 == 0:  # 2'şer buton yan yana, daha düzenli görünüm
            buttons.append([])
        buttons[-1].append(
            InlineKeyboardButton(
                text=_[f"H_B_{i}"],
                callback_data=f"help_callback hb{i}"
            )
        )

    # 🔹 En alt satırda Menü ve Kapat butonları
    buttons.append(
        [
            InlineKeyboardButton(
                text="🌊 Menü",
                callback_data="back_to_main"
            ),
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data="close"
            )
        ]
    )
    return InlineKeyboardMarkup(buttons)


def help_back_markup(_):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["BACK_BUTTON"],
                    callback_data="open_help"
                ),
                InlineKeyboardButton(
                    text=_["CLOSE_BUTTON"],
                    callback_data="close"
                ),
            ]
        ]
    )


def private_help_panel(_):
    return [
        [
            InlineKeyboardButton(
                text=_["S_B_3"],
                url="https://t.me/{0}?start=help".format(app.username)
            )
        ]
    ]