from pyrogram import filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message
from HasiiMusic import app


@app.on_message(filters.command("id"))
async def get_id(client, message: Message):
    chat = message.chat
    user = message.from_user
    reply = message.reply_to_message
    out = []

    # 📩 Mesaj ID'si
    if message.link:
        out.append(f"**[Mesaj ID:]({message.link})** `{message.id}`")
    else:
        out.append(f"**Mesaj ID:** `{message.id}`")

    # 👤 Kullanıcı ID'si
    out.append(f"**[Kullanıcı ID:](tg://user?id={user.id})** `{user.id}`")

    # 🎯 Belirli bir kullanıcı sorgulandıysa (/id @kullanici)
    if len(message.command) == 2:
        try:
            target = message.text.split(maxsplit=1)[1]
            target_user = await client.get_users(target)
            out.append(f"**[Hedef Kullanıcı ID:](tg://user?id={target_user.id})** `{target_user.id}`")
        except Exception:
            return await message.reply_text("❌ Bu kullanıcı bulunamadı.", quote=True)

    # 💬 Sohbet ID'si
    if chat.username and chat.type != "private":
        out.append(f"**[Sohbet ID:](https://t.me/{chat.username})** `{chat.id}`")
    else:
        out.append(f"**Sohbet ID:** `{chat.id}`")

    # 🔁 Yanıtlanan mesaj bilgileri
    if reply:
        if reply.link:
            out.append(f"**[Yanıtlanan Mesaj ID:]({reply.link})** `{reply.id}`")
        else:
            out.append(f"**Yanıtlanan Mesaj ID:** `{reply.id}`")

        if reply.from_user:
            out.append(
                f"**[Yanıtlanan Kullanıcı ID:](tg://user?id={reply.from_user.id})** `{reply.from_user.id}`"
            )

        if reply.forward_from_chat:
            out.append(
                f"📢 İletilen kanal **{reply.forward_from_chat.title}** kimliği: `{reply.forward_from_chat.id}`"
            )

        if reply.sender_chat:
            out.append(f"🧾 Yanıtın gönderildiği kanal/sohbet ID: `{reply.sender_chat.id}`")

    # ✅ Yanıtı gönder
    await message.reply_text(
        "\n".join(out),
        disable_web_page_preview=True,
        parse_mode=ParseMode.MARKDOWN,
    )