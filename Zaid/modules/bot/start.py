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

class Data:
    donate_button = [InlineKeyboardButton("Donate", callback_data="donate")]
    generate_single_button = [InlineKeyboardButton("Basic Guide", callback_data="guide")]

    home_buttons = [
        generate_single_button,
        [InlineKeyboardButton("Return Home", callback_data="home")]
    ]

    back_buttons = [
        donate_button,
        [InlineKeyboardButton("Return Home", callback_data="home")]
    ]

    guide_buttons = [[InlineKeyboardButton("Return Home", callback_data="home")]]

    buttons = [
        generate_single_button,
        [InlineKeyboardButton("Owner", url=OWNER_LINK)],
        [
            InlineKeyboardButton("How to use", callback_data="help"),
            InlineKeyboardButton("About", callback_data="about")
        ],
        [InlineKeyboardButton("Developer", url=OWNER_LINK)],
    ]

    START = f"""
**Hey, I am SAMAR Userbot**
Nice to meet you!

I am a powerful ID-userbot.
You can use me for fun features.

By: [@{OWNER_USERNAME}]({OWNER_LINK})
"""

    HELP = """
**Available commands**

/start - start the bot
/help - open help menu
/about - about the bot and owner
/add - auto-host the bot (login with phone)
/clone - clone via string session
/remove - logout from bot
"""

    GUIDE = f"""**Quick guide to host userbot**

1) Send /add to the bot
2) Send your phone number in international format (e.g. +917800000000)
3) Open Telegram app on that number → you will get login code (OTP)
4) Send OTP here **without spaces** e.g. `12345` (or with spaces `1 2 3 4 5` — both work now)

If 2FA is on, send that password next.

Support: [@{OWNER_USERNAME}]({OWNER_LINK})
"""

    ABOUT = f"""
**About this bot**

Telegram userbot host panel.

Language: Python
Owner / Developer: [@{OWNER_USERNAME}]({OWNER_LINK})
Owner ID: `{OWNER_ID}`
"""

    DONATE = f"""
Thanks for considering support.

Contact owner: [@{OWNER_USERNAME}]({OWNER_LINK})
"""


@app.on_message(filters.command("start") & filters.private)
async def start_handler(client: Client, message: Message):
    await client.send_photo(
        chat_id=message.chat.id,
        photo=ALIVE_PIC,
        caption=Data.START,
        reply_markup=InlineKeyboardMarkup(Data.buttons)
    )


@app.on_message(filters.command("help") & filters.private)
async def help_command(client: Client, message: Message):
    await message.reply_text(
        Data.HELP,
        reply_markup=InlineKeyboardMarkup(Data.home_buttons)
    )


@app.on_message(filters.command("about") & filters.private)
async def about_command(client: Client, message: Message):
    await message.reply_text(
        Data.ABOUT,
        reply_markup=InlineKeyboardMarkup(Data.home_buttons)
    )


@app.on_callback_query()
async def callback_handler(client: Client, query: CallbackQuery):
    data = query.data
    if data == "home":
        await query.message.edit_media(
            media=InputMediaPhoto(ALIVE_PIC, caption=Data.START),
            reply_markup=InlineKeyboardMarkup(Data.buttons)
        )
    elif data == "help":
        await query.message.edit_text(
            Data.HELP,
            reply_markup=InlineKeyboardMarkup(Data.home_buttons)
        )
    elif data == "about":
        await query.message.edit_text(
            Data.ABOUT,
            reply_markup=InlineKeyboardMarkup(Data.home_buttons)
        )
    elif data == "donate":
        await query.message.edit_text(
            Data.DONATE,
            reply_markup=InlineKeyboardMarkup(Data.guide_buttons)
        )
    elif data == "guide":
        await query.message.edit_text(
            Data.GUIDE,
            reply_markup=InlineKeyboardMarkup(Data.back_buttons)
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
                plugins=dict(root="Zaid/modules")
            )
            await client.start()
            active_sessions.append(client)
            logging.info(f"Started session for user {uid}")
        except Exception as e:
            logging.error(f"Failed to start session for user {uid}: {e}")


@app.on_message(filters.command("clone") & filters.private)
async def clone(bot: app, msg: Message):
    text = await msg.reply("FIRST GEN SESSION\n\n/clone session\n\nOR use /add for auto-host")
    if len(msg.command) < 2:
        return
    phone = msg.command[1]
    try:
        await text.edit("Please wait...")
        client = Client(
            name="Melody",
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=phone,
            plugins=dict(root="Zaid/modules"),
        )
        await client.start()
        user = await client.get_me()
        await msg.reply(f"Ready\n\nBot added successfully\n\n{user.first_name}")
    except Exception as e:
        await msg.reply(f"**ERROR:** `{str(e)}`\nPress /start to try again.")


@app.on_message(filters.command("add") & filters.private)
async def add_session_command(client, message: Message):
    user_id = message.from_user.id
    await message.reply(
        "Please send your phone number in international format\n(e.g. +918200000009):"
    )
    user_sessions[user_id] = {"step": "awaiting_phone"}


@app.on_message(filters.command("remove") & filters.private)
async def remove_session(_, msg: Message):
    uid = msg.from_user.id
    session_data = sessions_col.find_one({"_id": uid})
    if not session_data:
        return await msg.reply("No active session found.")

    try:
        for c in list(active_sessions):
            if c.name == f"AutoClone_{uid}":
                await c.stop()
                active_sessions.remove(c)
                break
        sessions_col.delete_one({"_id": uid})
        await msg.reply("Your session removed successfully.")
    except Exception as e:
        await msg.reply(f"Error removing session:\n`{e}`")


@app.on_message(filters.private & filters.text & ~filters.command(["start", "help", "about", "add", "remove", "clone"]))
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
        client = Client(name=f"gen_{uid}", api_id=API_ID, api_hash=API_HASH, in_memory=True)
        session.update({"phone": phone, "client": client})
        try:
            await client.connect()
            sent = await client.send_code(phone)
            session["phone_code_hash"] = sent.phone_code_hash
            session["step"] = "awaiting_otp"
            await msg.reply(
                "OTP sent by Telegram.\n\n"
                "1) Open Telegram on THAT phone number\n"
                "2) Check login code / notification\n"
                "3) Send code here as `12345` (spaces optional)"
            )
        except Exception as e:
            await msg.reply(
                f"Failed to send OTP:\n`{e}`\n\nTry again with /add\n"
                "Tips: correct +country code, wait 1–2 min if flood, check Telegram app not only SMS."
            )
            try:
                await client.disconnect()
            except Exception:
                pass
            user_sessions.pop(uid, None)

    elif step == "awaiting_otp":
        # accept both "12345" and "1 2 3 4 5"
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
            return await msg.reply("2FA enabled. Send your cloud password.")
        except Exception as e:
            await msg.reply(f"Sign-in failed:\n`{e}`\nTry again /add")
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
            await msg.reply(f"Wrong password:\n`{e}`\nTry again /add")
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
            f"Logged in as **{user.first_name}**.\n\n"
            f"Session string:\n`{string}`\n\n"
            f"Auto-host started.\nTo remove: /remove"
        )
    except Exception as e:
        await msg.reply(f"Final step failed:\n`{e}`\nTry /add again")
    finally:
        try:
            await client.disconnect()
        except Exception:
            pass
        user_sessions.pop(uid, None)
