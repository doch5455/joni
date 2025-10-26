from pyrogram.types import InlineKeyboardButton
import time
from HasiiMusic.utils.formatters import time_to_seconds

LAST_UPDATE_TIME = {}


def should_update_progress(chat_id):
    now = time.time()
    last = LAST_UPDATE_TIME.get(chat_id, 0)
    if now - last >= 6:
        LAST_UPDATE_TIME[chat_id] = now
        return True
    return False


def generate_progress_bar(played_sec, duration_sec):
    if duration_sec == 0:
        percentage = 0
    else:
        percentage = min((played_sec / duration_sec) * 100, 100)

    bar_length = 8
    filled = int(round(bar_length * percentage / 70))
    return "▰" * filled + "▱" * (bar_length - filled)


# 🔷 Sadece kapatma ve Mavi Duyuru butonlarını içeren düzen
def stream_markup_timer(_, chat_id, played, dur):
    if not should_update_progress(chat_id):
        return None

    played_sec = time_to_seconds(played)
    duration_sec = time_to_seconds(dur)
    bar = generate_progress_bar(played_sec, duration_sec)

    return [
        [InlineKeyboardButton(text=f"{played} {bar} {dur}", callback_data="GetTimer")],
        [
            InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close"),
            InlineKeyboardButton(text="💙 Mavi Duyuru", url="@MaviDuyuru"),
        ],
    ]


def stream_markup(_, chat_id):
    return [
        [
            InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close"),
            InlineKeyboardButton(text="💙 Mavi Duyuru", url="@maviduyuru"),
        ]
    ]


def track_markup(_, videoid, user_id, channel, fplay):
    return [
        [
            InlineKeyboardButton(
                text=_["P_B_1"],
                callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text=_["P_B_2"],
                callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}",
            ),
        ],
        [
            InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data=f"forceclose {videoid}|{user_id}"),
            InlineKeyboardButton(text="💙 Mavi Duyuru", url="@MaviDuyuru"),
        ],
    ]


def playlist_markup(_, videoid, user_id, ptype, channel, fplay):
    return [
        [
            InlineKeyboardButton(
                text=_["P_B_1"],
                callback_data=f"TuneViaPlaylists {videoid}|{user_id}|{ptype}|a|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text=_["P_B_2"],
                callback_data=f"TuneViaPlaylists {videoid}|{user_id}|{ptype}|v|{channel}|{fplay}",
            ),
        ],
        [
            InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data=f"forceclose {videoid}|{user_id}"),
            InlineKeyboardButton(text="💙 Mavi Duyuru", url="@MaviDuyuru"),
        ],
    ]


def livestream_markup(_, videoid, user_id, mode, channel, fplay):
    return [
        [
            InlineKeyboardButton(
                text=_["P_B_3"],
                callback_data=f"LiveStream {videoid}|{user_id}|{mode}|{channel}|{fplay}",
            )
        ],
        [
            InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data=f"forceclose {videoid}|{user_id}"),
            InlineKeyboardButton(text="💙 Mavi Duyuru", url="@MaviDuyuru"),
        ],
    ]


def slider_markup(_, videoid, user_id, query, query_type, channel, fplay):
    short_query = query[:20]
    return [
        [
            InlineKeyboardButton(
                text=_["P_B_1"],
                callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text=_["P_B_2"],
                callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}",
            ),
        ],
        [
            InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data=f"forceclose {short_query}|{user_id}"),
            InlineKeyboardButton(text="💙 Mavi Duyuru", url="@MaviDuyuru"),
        ],
    ]