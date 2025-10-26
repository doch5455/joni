import asyncio
import random
import urllib.parse
from pyrogram import filters, errors, types
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from typing import Optional

from config import LOGGER_ID
from HasiiMusic import app

BOT_BILGI: Optional[types.User] = None
BOT_ID: Optional[int] = None

FOTO = "https://files.catbox.moe/139oue.png"

def _gecerli_url(url: Optional[str]) -> bool:
    if not url:
        return False
    try:
        parsed = urllib.parse.urlparse(url.strip())
        return parsed.scheme in ("http", "https", "tg") and (parsed.netloc or parsed.path)
    except Exception:
        return False

async def _bot_bilgisi_al() -> None:
    global BOT_BILGI, BOT_ID
    if BOT_BILGI is None:
        try:
            BOT_BILGI = await app.get_me()
            BOT_ID = BOT_BILGI.id
        except Exception as e:
            print(f"Bot bilgisi alınamadı: {e}")

async def guvenli_foto_gonder(chat_id, foto, yazi, tuslar=None, deneme=3):
    for sayac in range(deneme):
        try:
            return await app.send_photo(
                chat_id=chat_id,
                photo=foto,
                caption=yazi,
                reply_markup=tuslar
            )
        except errors.FloodWait as e:
            await asyncio.sleep(e.value + 1)
        except errors.ButtonUrlInvalid:
            return await app.send_photo(
                chat_id=chat_id,
                photo=foto,
                caption=yazi
            )
        except Exception as e:
            if sayac == deneme - 1:
                raise
            await asyncio.sleep(1)

@app.on_message(filters.new_chat_members)
async def gruba_eklenme(_, message: Message):
    try:
        await _bot_bilgisi_al()
        if BOT_BILGI is None or BOT_ID is None:
            return

        chat = message.chat
        try:
            davet_linki = await app.export_chat_invite_link(chat.id)
        except Exception:
            davet_linki = None

        for uye in message.new_chat_members:
            if uye.id != BOT_ID:
                continue

            uye_sayisi = "?"
            try:
                uye_sayisi = await app.get_chat_members_count(chat.id)
            except errors.FloodWait as fw:
                await asyncio.sleep(fw.value + 1)
                uye_sayisi = await app.get_chat_members_count(chat.id)
            except Exception:
                pass

            yazi = (
                "🎶 **Yeni Bir Gruba Eklendim!**\n\n"
                "❅─────✧❅✦❅✧─────❅\n\n"
                f"📍 **Grup Adı:** `{chat.title}`\n"
                f"🆔 **Grup ID:** `{chat.id}`\n"
                f"👥 **Üye Sayısı:** `{uye_sayisi}`\n"
                f"🔗 **Davet Linki:** [Tıkla]({davet_linki or 'https://t.me/'})\n"
                f"👤 **Ekleyen:** {message.from_user.mention if message.from_user else 'Bilinmiyor'}"
            )

            tuslar = None
            if _gecerli_url(davet_linki):
                tuslar = InlineKeyboardMarkup(
                    [[InlineKeyboardButton("👀 Gruba Git", url=davet_linki.strip())]]
                )

            await guvenli_foto_gonder(
                LOGGER_ID,
                foto=FOTO,
                yazi=yazi,
                tuslar=tuslar
            )
    except Exception as e:
        print(f"Gruba eklenme logu gönderilemedi: {e}")

@app.on_message(filters.left_chat_member)
async def gruptan_cikma(_, message: Message):
    try:
        await _bot_bilgisi_al()
        if BOT_BILGI is None or BOT_ID is None:
            return

        if message.left_chat_member.id != BOT_ID:
            return

        kaldiran = message.from_user.mention if message.from_user else "**Bilinmeyen Kullanıcı**"
        chat = message.chat

        metin = (
            "📤 **Bot Bir Gruptan Çıkarıldı!**\n\n"
            f"📍 **Grup Adı:** `{chat.title}`\n"
            f"🆔 **Grup ID:** `{chat.id}`\n"
            f"👤 **Kaldıran:** {kaldiran}\n"
            f"🤖 **Bot:** @{BOT_BILGI.username}"
        )

        for deneme in range(3):
            try:
                await app.send_message(LOGGER_ID, metin)
                break
            except errors.FloodWait as e:
                await asyncio.sleep(e.value + 1)
            except Exception as e:
                if deneme == 2:
                    print(f"Çıkış mesajı gönderilemedi: {e}")
    except Exception as e:
        print(f"Gruptan çıkış işlemi hatası: {e}")