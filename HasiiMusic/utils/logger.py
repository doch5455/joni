from pyrogram.enums import ParseMode
from HasiiMusic import app
from HasiiMusic.utils.database import is_on_off
from HasiiMusic.utils.database.memorydatabase import get_active_chats  # aktif sohbetleri saymak için
from config import LOGGER_ID


async def play_logs(message, streamtype, query: str = None):
    if await is_on_off(2):
        if query is None:
            try:
                query = message.text.split(None, 1)[1]
            except Exception:
                query = "—"

        # 🔹 Aktif sesli sohbet sayısı alınır
        try:
            active_chats = await get_active_chats()
            active_count = len(active_chats)
        except Exception:
            active_count = 0

        log_text = f"""
<b>🎧 {app.mention} - Oynatma Kaydı</b>

<b>📍 Sohbet Adı:</b> {message.chat.title}
<b>🆔 Sohbet ID:</b> <code>{message.chat.id}</code>
<b>👤 Kullanıcı:</b> {message.from_user.mention}
<b>🔎 Arama:</b> {query}
<b>🎬 Tür:</b> {streamtype}

<b>📡 Aktif Sesli Sohbet Sayısı:</b> <code>{active_count}</code>
"""

        # Sadece log grubundan farklıysa gönder
        if message.chat.id != LOGGER_ID:
            try:
                await app.send_message(
                    chat_id=LOGGER_ID,
                    text=log_text,
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True,
                )
            except Exception as e:
                print(f"Log gönderilemedi: {e}")