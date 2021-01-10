from bot import EMILIA
from pyrogram import filters

HELP_TEXT = """
**Available Commands:**
- **/anime <anime_name>**
- **/manga <manga_name>**
- **/character <character_name>**
- **/schedule <day>**
"""

@EMILIA.on_message(filters.command(["help"], prefixes = "/") & ~filters.edited)
async def help(client, message):
    await EMILIA.send_message(chat_id = message.chat.id, text = HELP_TEXT, parse_mode = "markdown")