import os
from os import getenv
from dotenv import load_dotenv

if os.path.exists("local.env"):
    load_dotenv("local.env")
elif os.path.exists(".env"):
    load_dotenv(".env")

API_ID = int(getenv("API_ID", "34979297") or "34979297")
API_HASH = getenv("API_HASH", "0e45dd9855674f34f91705734d7642b4") or "0e45dd9855674f34f91705734d7642b4"

SUDO_USERS = list(map(int, getenv("SUDO_USERS", "8841848847").split()))
OWNER_ID = int(getenv("OWNER_ID", "8841848847"))
MONGO_URL = getenv("MONGO_URL")
BOT_TOKEN = getenv("BOT_TOKEN", "")
ALIVE_PIC = getenv("ALIVE_PIC", "https://files.catbox.moe/lo4efn.jpg")
ALIVE_TEXT = getenv("ALIVE_TEXT", "SAMAR Userbot")
PM_LOGGER = getenv("PM_LOGGER")
LOG_GROUP = getenv("LOG_GROUP", "-1004318913888")
GIT_TOKEN = getenv("GIT_TOKEN")
REPO_URL = getenv("REPO_URL", "https://github.com/tsamarthakur515-spec/SAMAR_2USERBOT")
BRANCH = getenv("BRANCH", "master")

STRING_SESSION1 = getenv("STRING_SESSION1", "")
STRING_SESSION2 = getenv("STRING_SESSION2", "")
STRING_SESSION3 = getenv("STRING_SESSION3", "")
STRING_SESSION4 = getenv("STRING_SESSION4", "")
STRING_SESSION5 = getenv("STRING_SESSION5", "")
STRING_SESSION6 = getenv("STRING_SESSION6", "")
STRING_SESSION7 = getenv("STRING_SESSION7", "")
STRING_SESSION8 = getenv("STRING_SESSION8", "")
STRING_SESSION9 = getenv("STRING_SESSION9", "")
STRING_SESSION10 = getenv("STRING_SESSION10", "")
