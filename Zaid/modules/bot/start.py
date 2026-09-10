import logging
from pyrogram import Client, filters
from pyrogram.errors import SessionPasswordNeeded
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
**/add - ᴀᴜᴛᴏ-ʜᴏsᴛ ᴛʜᴇ ʙᴏᴛ**
**/clone - ᴄʟᴏɴᴇ ᴠɪᴀ sᴛʀɪɴɢ sᴇssɪᴏɴ**
**/remove - ʟᴏɢᴏᴜᴛ ғʀᴏᴍ ʙᴏᴛ**
"""

    GUIDE = f"""**❖ ʜᴇʏ ᴅᴇᴀʀ, ᴛʜɪs ɪs ᴀ ǫᴜɪᴄᴋ ᴀɴᴅ sɪᴍᴘʟᴇ ɢᴜɪᴅᴇ ᴛᴏ ʜᴏsᴛɪɴɢ ᴜsᴇʀʙᴏᴛ**

**1) Sᴇɴᴅ /add ᴄᴏᴍᴍᴀɴᴅ ᴛᴏ ᴛʜᴇ ʙᴏᴛ **
**2) Sᴇɴᴅ ʏᴏᴜʀ ᴘʜᴏɴᴇ ɴᴜᴍʙᴇʀ ɪɴ ɪɴᴛᴇʀɴᴀᴛɪᴏɴᴀʟ ғᴏʀᴍᴀᴛ (ᴇ.ɢ. +917800000000)**
**3) ᴄʜᴇᴄᴋ ʏᴏᴜʀ ᴛᴇʟᴇɢʀᴀᴍ ᴀᴘᴘ ғᴏʀ OTP, ᴀɴᴅ sᴇɴᴅ ɪᴛ ʜᴇʀᴇ (sᴘᴀᴄᴇs ᴏᴘᴛɪᴏɴᴀʟ)**

**➤ ɪғ 2FA ᴏɴ, sᴇɴᴅ ᴛʜᴀᴛ ᴘᴀssᴡᴏʀᴅ ɴᴇxᴛ.**
**➤ ʏᴏᴜʀ ʙᴏᴛ ᴡɪʟʟ ʙᴇ ʜᴏsᴛᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ.**

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
    text = await msg.reply("❍ FIRST GEN SESSION\n\n𔓕 /clone session\n\n❍ OR - USE\n\n𔓕 /add ( ғᴏʀ ᴀᴜᴛᴏ-ʜᴏsᴛ )")
    if len(msg.command) < 2:
        return
    phone = msg.command[1]
    try:
        await text.edit("❖ ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ ᴀ ᴍɪɴᴜᴛᴇ")
        client = Client(
            name="Melody",
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=phone,
            plugins=dict(root="Zaid/modules"),
        )
        await client.start()
        user = await client.get_me()
        await msg.reply(
            f"❖ ɴᴏᴡ ʏᴏᴜ ᴀʀᴇ ʀᴇᴀᴅʏ\n\n❍ ʙᴏᴛ sᴜᴄᴄᴇssғᴜʟʟʏ ᴀᴅᴅᴇᴅ\n\n❖ {user.first_name}"
        )
    except Exception as e:
        await msg.reply(f"**ERROR:** `{str(e)}`\n ᴘʀᴇss /start ᴛᴏ sᴛᴀʀᴛ ᴀɢᴀɪɴ.")


@app.on_message(filters.command("add") & filters.private)
async def add_session_command(client, message: Message):
    user_id = message.from_user.id
    await message.reply(
        "📲 ᴘʟᴇᴀsᴇ sᴇɴᴅ ʏᴏᴜʀ ᴘʜᴏɴᴇ ɴᴜᴍʙᴇʀ ɪɴ ɪɴᴛᴇʀɴᴀᴛɪᴏɴᴀʟ ғᴏʀᴍᴀᴛ (e.g., +918200000009):"
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
        phone = msg.text.strip().replace(" ", "")
        if not phone.startswith("+"):
            await msg.reply("Number must start with + and country code. Example: +977...")
            return
        client = Client(
            name=f"gen_{uid}", api_id=API_ID, api_hash=API_HASH, in_memory=True
        )
        session.update({"phone": phone, "client": client})
        try:
            await client.connect()
            sent = await client.send_code(phone)
            session["phone_code_hash"] = sent.phone_code_hash
            session["step"] = "awaiting_otp"
            await msg.reply(
                "📨 OTP sᴇɴᴛ! ᴘʟᴇᴀsᴇ sᴇɴᴅ ɪɴ ᴛʜɪs ғᴏʀᴍᴀᴛ: `1 2 3 4 5` (sᴘᴀᴄᴇs ᴏᴘᴛɪᴏɴᴀʟ)"
            )
        except Exception as e:
            await msg.reply(
                f"❌ ғᴀɪʟᴇᴅ:\n`{e}`\nᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ /add"
            )
            try:
                await client.disconnect()
            except Exception:
                pass
            user_sessions.pop(uid, None)

    elif step == "awaiting_otp":
        otp = msg.text.strip().replace(" ", "")
        client = session["client"]
        try:
            await client.sign_in(
                phone_number=session["phone"],
                phone_code_hash=session["phone_code_hash"],
                phone_code=otp,
            )
        except SessionPasswordNeeded:
            session["step"] = "awaiting_2fa"
            return await msg.reply("🔐 sᴇɴᴅ ʏᴏᴜʀ 2FA ᴘᴀssᴡᴏʀᴅ.")
        except Exception as e:
            await msg.reply(f"❌ sɪɢɴ ɪɴ ғᴀɪʟᴇᴅ:\n`{e}`\n/add ᴀɢᴀɪɴ")
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
            await msg.reply(f"❌ ᴡʀᴏɴɢ ᴘᴀssᴡᴏʀᴅ:\n`{e}`\n/add ᴀɢᴀɪɴ")
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
            f"✅ ʟᴏɢɢᴇᴅ ɪɴ ᴀs **{user.first_name}**.\n\n"
            f"🔐 sᴇssɪᴏɴ:\n`{string}`\n\n"
            f"ᴀᴜᴛᴏ-ʜᴏsᴛ ᴏɴ.\n/remove sᴇɴᴅ ᴋᴀʀᴏ ʟᴏɢᴏᴜᴛ ᴋᴇ ʟɪʏᴇ."
        )
    except Exception as e:
        await msg.reply(f"❌ ғɪɴᴀʟ sᴛᴇᴘ ғᴀɪʟᴇᴅ:\n`{e}`\n/add ᴀɢᴀɪɴ")
    finally:
        try:
            await client.disconnect()
        except Exception:
            pass
        user_sessions.pop(uid, None)
