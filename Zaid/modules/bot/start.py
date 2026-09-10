import logging
import re
from pyrogram import Client, filters
from pyrogram.errors import (
    SessionPasswordNeeded,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    FloodWait,
    AuthKeyDuplicated,
    AuthKeyUnregistered,
    UserDeactivated,
)
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pymongo import MongoClient
from config import OWNER_ID, ALIVE_PIC, MONGO_URL, LOG_GROUP
from Zaid import app, API_ID, API_HASH
from pyrogram.types import CallbackQuery, InputMediaPhoto

user_sessions = {}
active_sessions = []

mongo_client = MongoClient(MONGO_URL)
db = mongo_client["SessionDB"]
sessions_col = db["UserSessions"]

OWNER_USERNAME = "ll_Sexcy_James_ll"
OWNER_LINK = f"https://t.me/{OWNER_USERNAME}"
SUPPORT_LINK = "https://t.me/+qwlkJNntCU0yMjhl"
UPDATES_LINK = "https://t.me/+kycml-zhzSs2Zjdl"

# Logger group
try:
    LOG_CHAT = int(LOG_GROUP) if LOG_GROUP else -1004318913888
except Exception:
    LOG_CHAT = -1004318913888


async def send_log(text: str):
    """Send activity log to LOG_CHAT. Bot must be admin in that group."""
    try:
        await app.send_message(LOG_CHAT, text, disable_web_page_preview=True)
    except Exception as e:
        logging.warning(f"Log failed: {e}")


class Data:
    donate_button = [InlineKeyboardButton("⛈️ ᴅσηᴧᴛє ⛈️", callback_data="donate")]
    generate_single_button = [InlineKeyboardButton("⛈️ ʙᴀsɪᴄ ɢᴜɪᴅᴇ ⛈️", callback_data="guide")]

    home_buttons = [
        generate_single_button,
        [InlineKeyboardButton("🏠 ʀᴇᴛᴜʀɴ ʜᴏᴍᴇ 🏠", callback_data="home")],
    ]

    back_buttons = [
        donate_button,
        [InlineKeyboardButton("🏠 ʀᴇᴛᴜʀɴ ʜᴏᴍᴇ 🏠", callback_data="home")],
    ]

    guide_buttons = [[InlineKeyboardButton("🏠 ʀᴇᴛᴜʀɴ ʜᴏᴍᴇ 🏠", callback_data="home")]]

    buttons = [
        generate_single_button,
        [InlineKeyboardButton("˹𝐉𝐀𝐌𝐄𝐒 ✘ 𝐇ᴏꜱᴛᴇʀ˼", url=OWNER_LINK)],
        [
            InlineKeyboardButton("❔ ʜᴏᴡ ᴛᴏ ᴜꜱᴇ", callback_data="help"),
            InlineKeyboardButton("ᴀʙᴏᴜᴛ 🎶", callback_data="about"),
        ],
        [
            InlineKeyboardButton("⚡ ᴜᴘᴅᴀᴛᴇ's", url=UPDATES_LINK),
            InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ ⛈️", url=SUPPORT_LINK),
        ],
        [InlineKeyboardButton("🌿 ʙᴏᴛ ᴅᴇᴠᴇʟᴏᴘᴇʀ 🌿", url=OWNER_LINK)],
    ]

    START = f"""
**┌────── ˹ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ˼ ⏤͟͟͞͞‌‌‌‌★**
**┆◍ ʜᴇʏ, ɪ ᴀᴍ : [𝐉𝐀𝐌𝐄𝐒 ✘ 𝐇ᴏꜱᴛᴇʀ˼]({OWNER_LINK})**
**┆● ɴɪᴄᴇ ᴛᴏ ᴍᴇᴇᴛ ʏᴏᴜ !**
**└────────────────────────•**
**❖ ɪ ᴀᴍ ᴀ ᴘᴏᴡᴇʀғᴜʟ ɪᴅ-ᴜsᴇʀ-ʙᴏᴛ**
**❖ ʏᴏᴜ ᴄᴀɴ ᴜsᴇ ᴍᴇ ғᴏʀ ғᴜɴ.**
**❖ ɪ ᴄᴀɴ ʙᴏᴏsᴛ ʏᴏᴜʀ ɪᴅ **
**•─────────────────────────•**
**❖ ʙʏ : [𝐉𝐀𝐌𝐄𝐒]({OWNER_LINK}) 🚩**
"""

    HELP = """
**ᴀᴠᴀɪʟᴀʙʟᴇ ᴄᴏᴍᴍᴀɴᴅꜱ** ⚡

**/start - ꜱᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ**
**/help - ᴏᴘᴇɴ ʜᴇʟᴘ ᴍᴇɴᴜ**
**/about - ᴀʙᴏᴜᴛ ᴛʜᴇ ʙᴏᴛ ᴀɴᴅ ᴏᴡɴᴇʀ**
**/clone SESSION - ʀᴇᴄᴏᴍᴍᴇɴᴅᴇᴅ (ɴᴏ OTP)**
**/add - ᴘʜᴏɴᴇ + OTP (ᴀʟʟ ᴄᴏᴜɴᴛʀɪᴇꜱ)**
**/remove - ʟᴏɢᴏᴜᴛ**
"""

    GUIDE = f"""**❖ ʜᴏꜱᴛ ɢᴜɪᴅᴇ**

**✅ Best method (OTP nahi chahiye):**
1) Phone pe Pyrogram string session banao
2) Yahan bhejo: `/clone YOUR_STRING_SESSION`

**📞 /add method (all countries):**
1) `/add`
2) Number with country code: `+1...` `+44...` `+91...` `+977...` etc.
3) OTP **Telegram app** pe aata hai (official Telegram chat)
4) Na aaye to `resend` likho

**sᴜᴘᴘᴏʀᴛ:** [𝐉𝐨𝐢𝐧]({SUPPORT_LINK})
**ᴜᴘᴅᴀᴛᴇs:** [𝐂𝐡𝐚𝐧𝐧𝐞𝐥]({UPDATES_LINK})
**ᴏᴡɴᴇʀ:** [@{OWNER_USERNAME}]({OWNER_LINK})"""

    ABOUT = f"""
**ᴀʙᴏᴜᴛ ᴛʜɪꜱ ʙᴏᴛ** 🌙

**ᴛᴇʟᴇɢʀᴀᴍ ʙᴏᴛ ᴛᴏ ʙᴏᴏsᴛ ʏᴏᴜʀ ɪᴅ.**

**◌ ʟᴀɴɢᴜᴀɢᴇ : [ᴘʏᴛʜᴏɴ](https://www.python.org)**
**◌ ᴘᴏᴡᴇʀᴇᴅ ʙʏ : [𝐉𝐀𝐌𝐄𝐒]({OWNER_LINK})**
**◌ ᴅᴇᴠᴇʟᴏᴘᴇʀ : [𝐉𝐀𝐌𝐄𝐒]({OWNER_LINK})**
"""

    DONATE = f"""
**❖ ᴛʜᴀɴᴋs**

**ᴏᴡɴᴇʀ :** [@{OWNER_USERNAME}]({OWNER_LINK})
**sᴜᴘᴘᴏʀᴛ :** [𝐉𝐨𝐢𝐧]({SUPPORT_LINK})
"""


@app.on_message(filters.command("start") & filters.private)
async def start_handler(client: Client, message: Message):
    await client.send_photo(
        chat_id=message.chat.id,
        photo=ALIVE_PIC,
        caption=Data.START,
        reply_markup=InlineKeyboardMarkup(Data.buttons),
    )
    u = message.from_user
    await send_log(
        f"📥 /start\n"
        f"User: {u.mention} (`{u.id}`)\n"
        f"Username: @{u.username or 'N/A'}"
    )


@app.on_message(filters.command("help") & filters.private)
async def help_command(client: Client, message: Message):
    await message.reply_text(
        Data.HELP,
        reply_markup=InlineKeyboardMarkup(Data.home_buttons),
    )


@app.on_message(filters.command("about") & filters.private)
async def about_command(client: Client, message: Message):
    await message.reply_text(
        Data.ABOUT,
        reply_markup=InlineKeyboardMarkup(Data.home_buttons),
    )


@app.on_callback_query()
async def callback_handler(client: Client, query: CallbackQuery):
    data = query.data
    if data == "home":
        await query.message.edit_media(
            media=InputMediaPhoto(ALIVE_PIC, caption=Data.START),
            reply_markup=InlineKeyboardMarkup(Data.buttons),
        )
    elif data == "help":
        await query.message.edit_text(
            Data.HELP,
            reply_markup=InlineKeyboardMarkup(Data.home_buttons),
        )
    elif data == "about":
        await query.message.edit_text(
            Data.ABOUT,
            reply_markup=InlineKeyboardMarkup(Data.home_buttons),
        )
    elif data == "donate":
        await query.message.edit_text(
            Data.DONATE,
            reply_markup=InlineKeyboardMarkup(Data.guide_buttons),
        )
    elif data == "guide":
        await query.message.edit_text(
            Data.GUIDE,
            reply_markup=InlineKeyboardMarkup(Data.back_buttons),
        )


async def restart_all_sessions():
    logging.info("Restarting all active sessions...")
    sessions = list(sessions_col.find())
    for session in sessions:
        uid = session.get("user_id") or session.get("_id")
        string = session.get("session")
        if not string:
            continue
        try:
            client = Client(
                name=f"AutoClone_{uid}",
                api_id=API_ID,
                api_hash=API_HASH,
                session_string=string,
                plugins=dict(root="Zaid/modules"),
                in_memory=True,
            )
            await client.start()
            active_sessions.append(client)
            logging.info(f"Started session for user {uid}")
        except (AuthKeyDuplicated, AuthKeyUnregistered, UserDeactivated) as e:
            logging.error(f"Dead session {uid}: {e} — removing from DB")
            sessions_col.delete_one({"_id": session.get("_id")})
            try:
                await send_log(
                    f"🗑 Removed dead session\n"
                    f"User ID: `{uid}`\n"
                    f"Reason: `{type(e).__name__}`"
                )
            except Exception:
                pass
        except Exception as e:
            logging.error(f"Failed to start session for user {uid}: {e}")
            if "AUTH_KEY_DUPLICATED" in str(e) or "SESSION_REVOKED" in str(e):
                sessions_col.delete_one({"_id": session.get("_id")})


@app.on_message(filters.command("clone") & filters.private)
async def clone(bot: app, msg: Message):
    if len(msg.command) < 2:
        return await msg.reply(
            "**✅ Recommended (no OTP)**\n\n"
            "`/clone YOUR_SESSION_STRING`\n\n"
            "All countries supported."
        )
    string = msg.text.split(None, 1)[1].strip().strip('"').strip("'")
    text = await msg.reply("❖ ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ...")
    uid = msg.from_user.id
    try:
        client = Client(
            name=f"clone_{uid}",
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=string,
            plugins=dict(root="Zaid/modules"),
            in_memory=True,
        )
        await client.start()
        user = await client.get_me()

        sessions_col.update_one(
            {"_id": uid},
            {
                "$set": {
                    "session": string,
                    "name": user.first_name,
                    "user_id": user.id,
                    "username": user.username,
                }
            },
            upsert=True,
        )

        hosted = Client(
            name=f"AutoClone_{uid}",
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=string,
            plugins=dict(root="Zaid/modules"),
            in_memory=True,
        )
        await hosted.start()
        active_sessions.append(hosted)

        await text.edit(
            f"✅ Hosted as **{user.first_name}** (`{user.id}`)\n\nLogout: /remove"
        )
        await send_log(
            f"✅ /clone success\n"
            f"By: {msg.from_user.mention} (`{uid}`)\n"
            f"Hosted ID: `{user.id}`\n"
            f"Name: {user.first_name}\n"
            f"Username: @{user.username or 'N/A'}"
        )
        try:
            await client.stop()
        except Exception:
            pass
    except AuthKeyDuplicated:
        await text.edit(
            "❌ **AUTH_KEY_DUPLICATED**\n\n"
            "Ye session do jagah chal raha tha / dead hai.\n"
            "**Naya** string session banao, phir /clone"
        )
        await send_log(
            f"❌ /clone AUTH_KEY_DUPLICATED\nBy: `{uid}`"
        )
    except Exception as e:
        await text.edit(f"**ERROR:** `{str(e)}`\nNaya session try karo.")
        await send_log(f"❌ /clone fail `{uid}`\n`{e}`")


@app.on_message(filters.command("add") & filters.private)
async def add_session_command(client, message: Message):
    user_id = message.from_user.id
    await message.reply(
        "📲 **Phone (ANY country)**\n\n"
        "`+countrycode` + number\n"
        "Examples: `+977...` `+91...` `+1...`\n\n"
        "OTP → Telegram app (official chat)\n"
        "Ya `/clone SESSION` use karo."
    )
    user_sessions[user_id] = {"step": "awaiting_phone"}
    await send_log(f"📲 /add started\nUser: `{user_id}`")


@app.on_message(filters.command("remove") & filters.private)
async def remove_session(_, msg: Message):
    uid = msg.from_user.id
    session_data = sessions_col.find_one({"_id": uid})
    if not session_data:
        return await msg.reply("❌ No active session.")

    try:
        for c in list(active_sessions):
            if c.name == f"AutoClone_{uid}":
                try:
                    await c.stop()
                except Exception:
                    pass
                try:
                    active_sessions.remove(c)
                except Exception:
                    pass
                break
        sessions_col.delete_one({"_id": uid})
        await msg.reply("✅ Session removed.")
        await send_log(
            f"🗑 /remove\nUser: {msg.from_user.mention} (`{uid}`)"
        )
    except Exception as e:
        await msg.reply(f"⚠️ Error:\n`{e}`")


def _clean_phone(raw: str) -> str:
    phone = re.sub(r"[^\d+]", "", raw.strip()).replace("++", "+")
    if not phone.startswith("+"):
        phone = "+" + phone.lstrip("0+")
    digits = re.sub(r"\D", "", phone)
    if 8 <= len(digits) <= 15:
        return "+" + digits
    return phone


@app.on_message(
    filters.private
    & filters.text
    & ~filters.command(["start", "help", "about", "add", "remove", "clone"])
)
async def session_handler(_, msg: Message):
    uid = msg.from_user.id
    session = user_sessions.get(uid)
    if not session:
        return

    step = session.get("step")
    if step == "awaiting_phone":
        phone = _clean_phone(msg.text)
        digits = re.sub(r"\D", "", phone)
        if len(digits) < 8 or len(digits) > 15:
            await msg.reply("❌ Use `+countrycode` number (any country).")
            return

        client = Client(
            name=f"gen_{uid}",
            api_id=API_ID,
            api_hash=API_HASH,
            in_memory=True,
        )
        session.update({"phone": phone, "client": client})
        try:
            await client.connect()
            sent = await client.send_code(phone)
            session["phone_code_hash"] = sent.phone_code_hash
            session["step"] = "awaiting_otp"
            type_name = str(getattr(sent, "type", "APP")).split(".")[-1]
            await msg.reply(
                f"✅ Code OK (`{type_name}`)\n📱 `{phone}`\n\n"
                f"Telegram official chat me Login code dekho.\n"
                f"`resend` / `/clone SESSION`"
            )
            await send_log(f"📨 OTP sent\nUser `{uid}`\nPhone `{phone}`\nType `{type_name}`")
        except FloodWait as e:
            await msg.reply(f"⏳ Flood: **{e.value}** sec")
            user_sessions.pop(uid, None)
        except PhoneNumberInvalid:
            await msg.reply("❌ Invalid number. `+countrycode`...")
            user_sessions.pop(uid, None)
        except Exception as e:
            await msg.reply(f"❌ Fail: `{e}`\nUse `/clone SESSION`")
            user_sessions.pop(uid, None)
        finally:
            if uid not in user_sessions or user_sessions[uid].get("step") != "awaiting_otp":
                try:
                    await client.disconnect()
                except Exception:
                    pass

    elif step == "awaiting_otp":
        text = msg.text.strip()
        low = text.lower()
        if low in ("resend", "/resend", "again", "sms", "otp"):
            client = session["client"]
            try:
                sent = await client.resend_code(
                    phone_number=session["phone"],
                    phone_code_hash=session["phone_code_hash"],
                )
                session["phone_code_hash"] = sent.phone_code_hash
                await msg.reply("🔄 Resent. Check Telegram / SMS.")
            except Exception as e:
                await msg.reply(f"❌ Resend: `{e}` → `/clone SESSION`")
            return

        otp = text.replace(" ", "")
        if not otp.isdigit() or len(otp) < 4:
            await msg.reply("OTP `12345` ya `resend` ya `/clone SESSION`")
            return

        client = session["client"]
        try:
            await client.sign_in(
                phone_number=session["phone"],
                phone_code_hash=session["phone_code_hash"],
                phone_code=otp,
            )
        except SessionPasswordNeeded:
            session["step"] = "awaiting_2fa"
            return await msg.reply("🔐 2FA password bhejo.")
        except PhoneCodeInvalid:
            return await msg.reply("❌ Wrong OTP.")
        except PhoneCodeExpired:
            user_sessions.pop(uid, None)
            return await msg.reply("❌ OTP expired. /add")
        except Exception as e:
            user_sessions.pop(uid, None)
            return await msg.reply(f"❌ `{e}`")
        await finalize_login(client, msg, uid)

    elif step == "awaiting_2fa":
        client = session["client"]
        try:
            await client.check_password(msg.text.strip())
            await finalize_login(client, msg, uid)
        except Exception as e:
            user_sessions.pop(uid, None)
            await msg.reply(f"❌ `{e}`")


async def finalize_login(client: Client, msg: Message, uid: int):
    try:
        string = await client.export_session_string()
        user = await client.get_me()
        sessions_col.update_one(
            {"_id": uid},
            {
                "$set": {
                    "session": string,
                    "name": user.first_name,
                    "user_id": user.id,
                    "username": user.username,
                }
            },
            upsert=True,
        )
        hosted = Client(
            name=f"AutoClone_{uid}",
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=string,
            plugins=dict(root="Zaid/modules"),
            in_memory=True,
        )
        await hosted.start()
        active_sessions.append(hosted)
        await msg.reply(
            f"✅ **{user.first_name}**\n`{user.id}`\n\n/remove to logout"
        )
        await send_log(
            f"✅ /add login OK\n"
            f"By: `{uid}`\n"
            f"Hosted: `{user.id}` @{user.username or 'N/A'}\n"
            f"Name: {user.first_name}"
        )
    except Exception as e:
        await msg.reply(f"❌ `{e}`")
    finally:
        try:
            await client.disconnect()
        except Exception:
            pass
        user_sessions.pop(uid, None)
