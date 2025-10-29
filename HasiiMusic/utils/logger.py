import psutil
from pyrogram.enums import ParseMode
from HasiiMusic import app
from HasiiMusic.utils.database import (
    get_served_chats,
    get_active_chats,
    get_active_video_chats,
    is_on_off,
)
from config import LOGGER_ID


def colorize(value: float) -> str:
    """CPU/RAM/Disk değerini renkli emoji ile döndürür."""
    if value <= 50:
        return f"🟢 {value}%"
    elif value <= 75:
        return f"🟡 {value}%"
    else:
        return f"🔴 {value}%"


async def play_logs(message, streamtype: str, query: str = None):
    """
    Oynatma başlatıldığında log kanalına minimal ama detaylı sistem raporu gönderir.
    (CPU, RAM, Disk, grup bilgileri, kullanıcı bilgileri, oynatma sorgusu vb.)
    """

    # Log sistemi açık mı kontrol et
    if not await is_on_off(2):
        return

    # Sorgu (query)
    if query is None:
        try:
            query = message.text.split(None, 1)[1]
        except Exception:
            query = "—"

    # Grup linki (gizli gruplar için export)
    if message.chat.username:
        chat_link = f"https://t.me/{message.chat.username}"
    else:
        try:
            invite_link = await app.export_chat_invite_link(message.chat.id)
            chat_link = invite_link
        except Exception:
            chat_link = "🔗 Link alınamadı"

    # Grup / kullanıcı bilgileri
    chat_title = getattr(message.chat, "title", "Bilinmeyen Sohbet")
    user_mention = getattr(message.from_user, "mention", "Bilinmeyen Kullanıcı")
    user_username = (
        f"@{message.from_user.username}"
        if message.from_user and message.from_user.username
        else "Yok"
    )

    # Sistem bilgileri
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    cpu_colored = colorize(cpu)
    ram_colored = colorize(ram)
    disk_colored = colorize(disk)

    toplam_grup = len(await get_served_chats())
    aktif_sesli = len(await get_active_chats())
    aktif_video = len(await get_active_video_chats())

    tarih = message.date.strftime("%d.%m.%Y • %H:%M:%S")

    # ───────────────────────────────────────────────────────────────
    #  LOG MESAJI (minimal ama detaylı)
    # ───────────────────────────────────────────────────────────────
    logger_text = f"""
<b>🎧 {app.mention} ᴘʟᴀʏ ʟᴏɢ</b>

<b>🏷 Chat :</b> <a href="{chat_link}">{chat_title}</a> <code>[{message.chat.id}]</code>
<b>👥 Üye Sayısı:</b> <code>{await app.get_chat_members_count(message.chat.id)}</code>

<b>👤 Kullanıcı:</b> {user_mention}
<b>🔖 Kullanıcı Adı:</b> {user_username}
<b>🆔 ID:</b> <code>{message.from_user.id if message.from_user else '—'}</code>

<b>🎹 Sorgu:</b> <code>{query}</code>
<b>🎧 Tür:</b> <code>{streamtype}</code>

<b>💻 Sistem Durumu</b>
🌍 <b>Toplam Grup:</b> <code>{toplam_grup}</code>
🎙 <b>Aktif Sesli:</b> <code>{aktif_sesli}</code>
📹 <b>Aktif Video:</b> <code>{aktif_video}</code>

🖥️ <b>CPU:</b> {cpu_colored}
🧠 <b>RAM:</b> {ram_colored}
🗄️ <b>Disk:</b> {disk_colored}

⏰ <b>Kayıt:</b> <code>{tarih}</code>
"""

    # ───────────────────────────────────────────────────────────────
    #  Log grubuna gönderim
    # ───────────────────────────────────────────────────────────────
    if message.chat.id != LOGGER_ID:
        try:
            await app.send_message(
                chat_id=LOGGER_ID,
                text=logger_text,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True,
            )

            # Kanal başlığını aktif sesli sayısı ile güncelle
            try:
                await app.set_chat_title(LOGGER_ID, f"🎶 Aktif Sesli: {aktif_sesli}")
            except Exception:
                pass

        except Exception as e:
            print(f"[Log Hatası] {e}")