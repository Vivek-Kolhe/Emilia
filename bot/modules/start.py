from bot import EMILIA
from pyrogram import filters

START_TEXT = """
Hey, I'm Emilia!
I can help you search for anime, manga, character info and much more.
Check /help for more.
"""

@EMILIA.on_message(filters.command(["start"], prefixes = "/") & ~filters.edited)
def start(client, message):
    EMILIA.send_message(chat_id = message.chat.id, text = START_TEXT)