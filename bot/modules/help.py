from bot import EMILIA
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

HELP_TEXT = """
**Available Commands:**
- **/mal_id <unique_id>**
- **/anime <anime_name>**
- **/manga <manga_name>**
- **/character <character_name>**
- **/schedule <day>**
"""

INFO_TEXT = """
Made with ❤️ by @pookie_0_0
"""

@EMILIA.on_message(filters.command(["help"], prefixes = "/") & ~filters.edited)
async def help(client, message):
    await EMILIA.send_message(chat_id = message.chat.id, text = HELP_TEXT, parse_mode = "markdown")

@EMILIA.on_message(filters.command(["about"], prefixes = "/") & ~filters.edited)
async def info(client, message):
    buttons = [
                [InlineKeyboardButton("⭐ Me?", url = "https://github.com/Vivek-Kolhe/Emilia"), InlineKeyboardButton("Report Issues", url = "https://t.me/pookie_0_0")]
              ]
    await EMILIA.send_message(chat_id = message.chat.id, text = INFO_TEXT, reply_markup = InlineKeyboardMarkup(buttons))
