from bot.config import Config
from pyrogram import Client, filters
from jikanpy import Jikan

API_ID = Config.API_ID
API_HASH = Config.API_HASH
BOT_TOKEN = Config.BOT_TOKEN

jikan = Jikan()
EMILIA = Client("Emilia", api_id = API_ID, api_hash = API_HASH, bot_token = BOT_TOKEN)
