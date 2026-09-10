import logging
import re
from pyrogram import Client, filters
from pyrogram.errors import (
    SessionPasswordNeeded,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    FloodWait,
)
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pymongo import MongoClient
from config import OWNER_ID, ALIVE_PIC, MONGO_URL
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

**Note:** SMS OTP Telegram rarely bhejta hai. APP type = code sirf us number ke Telegram pe.

**sᴜᴘᴘᴏʀᴛ:** [𝐉𝐨𝐢𝐧]({SUPPORT_LINK})
**ᴜᴘᴅᴀᴛᴇs:** [𝐂𝐡𝐚𝐧𝐧𝐞𝐥]({UPDATES_LINK})
**ᴏᴡɴᴇʀ:** [@{OWNER_USERNAME}]({OWNER_LINK})"""

    ABOUT = f"""
**ᴀʙᴏᴜᴛ ᴛʜɪꜱ ʙᴏᴛ** 🌙

**ᴛᴇʟᴇɢʀᴀᴍ ʙᴏᴛ ᴛᴏ ʙᴏᴏsᴛ ʏᴏᴜʀ ɪᴅ ᴡɪᴛʜ ʙᴇᴀᴜᴛɪғᴜʟ ᴀɴɪᴍᴀᴛɪᴏɴ.**

**sᴜᴘᴘᴏʀᴛᴇᴅ :- ʀᴇᴘʟʏ-ʀᴀɪᴅ, ɪᴅ-ᴄʟᴏɴᴇ, ʀᴀɪᴅ, sᴘᴀᴍ, ᴜsᴇʀ-ᴛᴀɢɢᴇʀ ᴇᴛᴄ.**

**◌ ʟᴀɴɢᴜᴀɢᴇ : [ᴘʏᴛʜᴏɴ](https://www.python.org)**
**◌ ᴘᴏᴡᴇʀᴇᴅ ʙʏ : [𝐉𝐀𝐌𝐄𝐒]({OWNER_LINK})**
**◌ ᴅᴇᴠᴇʟᴏᴘᴇʀ : [𝐉𝐀𝐌𝐄𝐒]({OWNER_LINK})**
"""

    DONATE = f"""
**❖ ʜᴇʏ, ᴛʜᴀɴᴋs ғᴏʀ sᴜᴘᴘᴏʀᴛ**

**ᴄᴏɴᴛᴀᴄᴛ ᴏᴡɴᴇʀ :** [@{OWNER_USERNAME}]({OWNER_LINK})
**sᴜᴘᴘᴏʀᴛ ɢᴄ :** [𝐉𝐨𝐢𝐧]({SUPPORT_LINK})
"""


@app.on_message(filters.command("start") & filters.private)
async def start_handler(client: Client, message: Message):
    await client.send_photo(
        chat_id=message.chat.id,
        photo=ALIVE_PIC,
        caption=Data.START,
        reply_markup=InlineKeyboardMarkup(Data.buttons),
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
    sessions = sessions_col.find()
    for session in sessions:
        try:
            uid = session["user_id"]
            string = session["session"]
            client = Client(
                name=f"AutoClone_{uid}",
                api_id=API_ID,
                api_hash=API_HASH,
                session_string=string,
                plugins=dict(root="Zaid/modules"),
            )
            await client.start()
            active_sessions.append(client)
            logging.info(f"Started session for user {uid}")
        except Exception as e:
            logging.error(f"Failed to start session for user {uid}: {e}")


@app.on_message(filters.command("clone") & filters.private)
async def clone(bot: app, msg: Message):
    if len(msg.command) < 2:
        return await msg.reply(
            "**✅ Recommended (no OTP)**\n\n"
            "1) Apne phone pe Pyrogram **string session** banao\n"
            "2) Yahan bhejo:\n"
            "`/clone YOUR_SESSION_STRING`\n\n"
            "OTP problem ho to yahi best method hai.\n"
            "All countries ke numbers ke sessions chalenge."
        )
    string = msg.text.split(None, 1)[1].strip()
    # strip accidental quotes
    string = string.strip('"').strip("'")
    text = await msg.reply("❖ ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ...")
    try:
        client = Client(
            name=f"clone_{msg.from_user.id}",
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=string,
            plugins=dict(root="Zaid/modules"),
            in_memory=True,
        )
        await client.start()
        user = await client.get_me()
        uid = msg.from_user.id

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
        )
        await hosted.start()
        active_sessions.append(hosted)

        await text.edit(
            f"✅ Hosted as **{user.first_name}** (`{user.id}`)\n\n"
            f"Logout: /remove"
        )
        try:
            await client.stop()
        except Exception:
            pass
    except Exception as e:
        await text.edit(
            f"**ERROR:** `{str(e)}`\n\n"
            f"Session invalid / expired. Naya string banao, phir /clone"
        )


@app.on_message(filters.command("add") & filters.private)
async def add_session_command(client, message: Message):
    user_id = message.from_user.id
    await message.reply(
        "📲 **Phone number bhejo (ANY country)**\n\n"
        "Format: `+` + country code + number\n"
        "Examples:\n"
        "`+97798xxxxxxxx` (Nepal)\n"
        "`+91xxxxxxxxxx` (India)\n"
        "`+1xxxxxxxxxx` (USA)\n"
        "`+44xxxxxxxxxx` (UK)\n"
        "`+8801xxxxxxxxx` (BD)\n\n"
        "⚠️ OTP usually **Telegram app** pe aata hai, SMS pe nahi.\n"
        "OTP na aaye → `resend` likho\n"
        "Ya best: string bana ke `/clone SESSION` use karo."
    )
    user_sessions[user_id] = {"step": "awaiting_phone"}


@app.on_message(filters.command("remove") & filters.private)
async def remove_session(_, msg: Message):
    uid = msg.from_user.id
    session_data = sessions_col.find_one({"_id": uid})
    if not session_data:
        return await msg.reply("❌ ɴᴏ ᴀᴄᴛɪᴠᴇ sᴇssɪᴏɴ ғᴏᴜɴᴅ.")

    try:
        for c in list(active_sessions):
            if c.name == f"AutoClone_{uid}":
                await c.stop()
                active_sessions.remove(c)
                break
        sessions_col.delete_one({"_id": uid})
        await msg.reply("✅ ʏᴏᴜʀ sᴇssɪᴏɴ ʀᴇᴍᴏᴠᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ.")
    except Exception as e:
        await msg.reply(f"⚠️ ᴇʀʀᴏʀ ʀᴇᴍᴏᴠɪɴɢ sᴇssɪᴏɴ:\n`{e}`")


def _clean_phone(raw: str) -> str:
    """E.164-ish: keep + and digits, any country."""
    phone = re.sub(r"[^\d+]", "", raw.strip())
    phone = phone.replace("++", "+")
    if not phone.startswith("+"):
        # user forgot + ; keep digits, require they fix with +
        phone = "+" + phone.lstrip("0+")
    # must be + then 8–15 digits total international
    digits = re.sub(r"\D", "", phone)
    if len(digits) < 8 or len(digits) > 15:
        return phone  # still return; validation below
    return "+" + digits


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
            await msg.reply(
                "❌ Number galat.\n"
                "Kisi bhi country ka number: `+` countrycode number\n"
                "Example: `+14155552671`"
            )
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

            code_type = getattr(sent, "type", None)
            type_name = str(code_type).split(".")[-1] if code_type else "APP"

            await msg.reply(
                f"✅ Code request OK (`{type_name}`)\n"
                f"📱 `{phone}` (all countries supported)\n\n"
                f"**OTP kahan:**\n"
                f"• Usi number ka Telegram → chat **Telegram** (official)\n"
                f"• Message: `Login code: XXXXX`\n\n"
                f"SMS tabhi aata hai jab Telegram type SMS bheje.\n"
                f"Nahi dikha? **`resend`** likho.\n"
                f"Phir bhi nahi? String bana ke `/clone SESSION`"
            )
        except FloodWait as e:
            await msg.reply(f"⏳ Flood: **{e.value}** sec baad /add")
            try:
                await client.disconnect()
            except Exception:
                pass
            user_sessions.pop(uid, None)
        except PhoneNumberInvalid:
            await msg.reply(
                "❌ Telegram is number ko invalid maanta hai.\n"
                "`+countrycode` sahi se bhejo (any country)."
            )
            try:
                await client.disconnect()
            except Exception:
                pass
            user_sessions.pop(uid, None)
        except Exception as e:
            await msg.reply(
                f"❌ OTP send fail:\n`{e}`\n\n"
                f"Try `/clone SESSION` instead (no OTP)."
            )
            try:
                await client.disconnect()
            except Exception:
                pass
            user_sessions.pop(uid, None)

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
                code_type = getattr(sent, "type", None)
                type_name = str(code_type).split(".")[-1] if code_type else "?"
                await msg.reply(
                    f"🔄 Resend OK (`{type_name}`)\n"
                    f"Telegram official chat / SMS check karo.\n"
                    f"Warna `/clone SESSION` use karo."
                )
            except FloodWait as e:
                await msg.reply(f"⏳ Resend wait: **{e.value}** sec")
            except Exception as e:
                await msg.reply(
                    f"❌ Resend fail: `{e}`\n"
                    f"Best option: `/clone YOUR_STRING_SESSION`"
                )
            return

        otp = text.replace(" ", "")
        if not otp.isdigit() or len(otp) < 4:
            await msg.reply(
                "OTP jaise `12345` bhejo.\n"
                "`resend` = naya code\n"
                "`/clone SESSION` = OTP skip"
            )
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
            return await msg.reply("🔐 2FA on. Cloud password bhejo.")
        except PhoneCodeInvalid:
            await msg.reply("❌ OTP galat. `resend` ya `/clone SESSION`")
            return
        except PhoneCodeExpired:
            await msg.reply("❌ OTP expire. /add ya /clone")
            try:
                await client.disconnect()
            except Exception:
                pass
            user_sessions.pop(uid, None)
            return
        except FloodWait as e:
            await msg.reply(f"⏳ Wait **{e.value}** sec")
            try:
                await client.disconnect()
            except Exception:
                pass
            user_sessions.pop(uid, None)
            return
        except Exception as e:
            await msg.reply(f"❌ Sign-in fail: `{e}`")
            try:
                await client.disconnect()
            except Exception:
                pass
            user_sessions.pop(uid, None)
            return
        await finalize_login(client, msg, uid)

    elif step == "awaiting_2fa":
        password = msg.text.strip()
        client = session["client"]
        try:
            await client.check_password(password)
            await finalize_login(client, msg, uid)
        except Exception as e:
            await msg.reply(f"❌ Password galat: `{e}`")
            try:
                await client.disconnect()
            except Exception:
                pass
            user_sessions.pop(uid, None)


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
        )
        await hosted.start()
        active_sessions.append(hosted)

        await msg.reply(
            f"✅ Logged in as **{user.first_name}**\n\n"
            f"Session:\n`{string}`\n\n"
            f"/remove for logout"
        )
    except Exception as e:
        await msg.reply(f"❌ Final fail: `{e}`")
    finally:
        try:
            await client.disconnect()
        except Exception:
            pass
        user_sessions.pop(uid, None)
