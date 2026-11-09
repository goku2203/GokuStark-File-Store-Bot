import os
import json
import logging
from logging.handlers import RotatingFileHandler


# Ellam values Render Environment variables la irundhu varum
def _get(name: str, default: str = "") -> str:
    return os.environ.get(name, default).strip()


def _get_int(name: str, default: int = 0) -> int:
    value = _get(name)
    if not value:
        return default
    try:
        return int(value)
    except ValueError:
        raise RuntimeError(f"Environment variable {name} must be a number, got: {value!r}")


def _get_bool(name: str, default: bool) -> bool:
    value = _get(name)
    if not value:
        return default
    return value.lower() in ("1", "true", "yes", "on")


def _get_int_list(name: str) -> list:
    value = _get(name)
    if not value:
        return []
    return [int(x) for x in value.replace(" ", "").split(",") if x]


# Bot Configuration
LOG_FILE_NAME = "bot.log"
PORT = _get_int("PORT", 10000)          # Render automatic ah PORT kudukkum
OWNER_ID = _get_int("OWNER_ID", 6629872386)

MSG_EFFECT = 5046509860389126442

SHORT_URL = _get("SHORT_URL", "gplinks.com")
SHORT_API = _get("SHORT_API", "")
SHORT_TUT = _get("SHORT_TUT", "https://t.me/howtoo1/7")

# Telegram credentials
SESSION = _get("SESSION", "yato")
TOKEN = _get("TOKEN")
API_ID = _get_int("API_ID", 0)
API_HASH = _get("API_HASH")
WORKERS = _get_int("WORKERS", 5)

# MongoDB
DB_URI = _get("DB_URI")
DB_NAME = _get("DB_NAME", "Cluster0")

# Force Subscription Channels [channel_id, request_enabled, timer_in_minutes]
# Env la JSON format: [[-1001234567890, true, 10]]
_fsubs_env = _get("FSUBS")
FSUBS = json.loads(_fsubs_env) if _fsubs_env else []

# Database Channel (Primary) - Telegram channel ID (example: -1001234567890)
DB_CHANNEL = _get_int("DB_CHANNEL", 0)

AUTO_DEL = _get_int("AUTO_DEL", 300)
ADMINS = _get_int_list("ADMINS")          # comma separated
DISABLE_BTN = _get_bool("DISABLE_BTN", True)
PROTECT = _get_bool("PROTECT", True)

# Required values check - missing na clear ah sollum
_missing = [
    name for name, value in (
        ("TOKEN", TOKEN), ("API_ID", API_ID), ("API_HASH", API_HASH),
        ("DB_URI", DB_URI), ("DB_CHANNEL", DB_CHANNEL),
    ) if not value
]
if _missing:
    raise RuntimeError(
        "Missing required environment variables: " + ", ".join(_missing)
        + " -> Render Dashboard > Environment la add pannunga."
    )
if not DB_URI.startswith(("mongodb://", "mongodb+srv://")):
    raise RuntimeError("DB_URI must start with mongodb:// or mongodb+srv://")

# Messages Configuration
MESSAGES = {
    "START": "<b>›› ʜᴇʏ!!, {first} ~ <blockquote>ʟᴏᴠᴇ ᴘᴏʀɴʜᴡᴀ? ɪ ᴀᴍ ᴍᴀᴅᴇ ᴛᴏ ʜᴇʟᴘ ʏᴏᴜ ᴛᴏ ғɪɴᴅ ᴡʜᴀᴛ ʏᴏᴜ aʀᴇ ʟᴏᴏᴋɪɴɢ ꜰᴏʀ.</blockquote></b>",
    "FSUB": "<b><blockquote>›› ʜᴇʏ ×</blockquote>\n  ʏᴏᴜʀ ғɪʟᴇ ɪs ʀᴇᴀᴅʏ ‼️ ʟᴏᴏᴋs ʟɪᴋᴇ ʏᴏᴜ ʜᴀᴠᴇɴ'ᴛ sᴜʙsᴄʀɪʙᴇᴅ ᴛᴏ ᴏᴜʀ ᴄʜᴀɴɴᴇʟs ʏᴇᴛ, sᴜʙsᴄʀɪʙᴇ ɴᴏᴡ ᴛᴏ ɢᴇᴛ ʏᴏᴜʀ ғɪʟᴇs</b>",
    "ABOUT": "<b>›› ғᴏʀ ᴍᴏʀᴇ: @Nova_Flix \n <blockquote expandable>›› ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ: <a href='https://t.me/codeflix_bots'>Cʟɪᴄᴋ ʜᴇʀᴇ</a> \n›› ᴏᴡɴᴇʀ: @ProYato\n›› ʟᴀɴɢᴜᴀɢᴇ: <a href='https://docs.python.org/3/'>Pʏᴛʜᴏɴ 3</a> \n›› ʟɪʙʀᴀʀʏ: <a href='https://docs.pyrogram.org/'>Pʏʀᴏɢʀᴀᴍ ᴠ2</a> \n›› ᴅᴀᴛᴀʙᴀsᴇ: <a href='https://www.mongodb.com/docs/'>Mᴏɴɢᴏ ᴅʙ</a> \n›› ᴅᴇᴠᴇʟᴏᴘᴇʀ: @cosmic_freak</b></blockquote>",
    "REPLY": "<b>For More Join - @Hanime_Arena</b>",
    "SHORT_MSG": "<b>📊 ʜᴇʏ {first}, \n\n‼️ ɢᴇᴛ ᴀʟʟ ꜰɪʟᴇꜱ ɪɴ ᴀ ꜱɪɴɢʟᴇ ʟɪɴᴋ ‼️\n\n ⌯ ʏᴏᴜʀ ʟɪɴᴋ ɪꜱ ʀᴇᴀᴅʏ, ᴋɪɴᴅʟʏ ᴄʟɪᴄᴋ ᴏɴ ᴏᴘᴇɴ ʟɪɴᴋ ʙᴜᴛᴛᴏɴ..</b>",
    "START_PHOTO": "https://graph.org/file/510affa3d4b6c911c12e3.jpg",
    "FSUB_PHOTO": "https://telegra.ph/file/7a16ef7abae23bd238c82-b8fbdcb05422d71974.jpg",
    "SHORT_PIC": "https://telegra.ph/file/7a16ef7abae23bd238c82-b8fbdcb05422d71974.jpg",
    "SHORT": "https://telegra.ph/file/8aaf4df8c138c6685dcee-05d3b183d4978ec347.jpg"
}


def LOGGER(name: str, client_name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    formatter = logging.Formatter(
        f"[%(asctime)s - %(levelname)s] - {client_name} - %(name)s - %(message)s",
        datefmt='%d-%b-%y %H:%M:%S'
    )
    file_handler = RotatingFileHandler(LOG_FILE_NAME, maxBytes=5_000_000, backupCount=2)
    file_handler.setFormatter(formatter)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    return logger
