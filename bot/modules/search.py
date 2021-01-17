from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from bot import EMILIA, jikan
from .mal import data_from_id

@EMILIA.on_message(filters.command(["anime"], prefixes = "/") & ~filters.edited)
async def get_anime(client, message):
    query = message.text.split(maxsplit = 1)
    if len(query) < 2:
        await EMILIA.send_message(chat_id = message.chat.id, text = "No search query found!\nExample:\n**/anime clannad**", parse_mode = "markdown")
        return
    try:
        temp = jikan.search("anime", query[-1])
        mal_id = temp["results"][0]["mal_id"]
        text, mal_url, trailer = data_from_id("anime", mal_id)
        if trailer:
            buttons = [
                        [InlineKeyboardButton("More Info!", url = mal_url), InlineKeyboardButton("Watch Trailer!", url = trailer)]
                        ]
        else:
            buttons = [
                        [InlineKeyboardButton("More Info!", url = mal_url)]
                        ]
        await EMILIA.send_message(chat_id = message.chat.id, text = text, parse_mode = "markdown", reply_markup = InlineKeyboardMarkup(buttons))
    except Exception as e:
        await EMILIA.send_message(chat_id = message.chat.id, text = e)

@EMILIA.on_message(filters.command(["manga"], prefixes = "/") & ~filters.edited)
async def get_manga(client, message):
    query = message.text.split(maxsplit = 1)
    if len(query) < 2:
        await EMILIA.send_message(chat_id = message.chat.id, text = "No search query found!\nExample:\n**/manga fairy tail**", parse_mode = "markdown")
        return
    try:
        temp = jikan.search("manga", query[-1])
        mal_id = temp["results"][0]["mal_id"]
        text, mal_url = data_from_id("manga", mal_id)
        buttons = [[InlineKeyboardButton("More Info!", url = mal_url)]]
        await EMILIA.send_message(chat_id = message.chat.id, text = text, parse_mode = "markdown", reply_markup = InlineKeyboardMarkup(buttons))
    except Exception as e:
        await EMILIA.send_message(chat_id = message.chat.id, text = e)

@EMILIA.on_message(filters.command(["character"], prefixes = "/") & ~filters.edited)
async def get_character(client, message):
    query = message.text.split(maxsplit = 1)
    if len(query) < 2:
        await EMILIA.send_message(chat_id = message.chat.id, text = "No search query found!\nExample:\n**/character hestia**", parse_mode = "markdown")
        return
    try:
        temp = jikan.search("character", query[-1])
        mal_id = temp["results"][0]["mal_id"]
        text, mal_url = data_from_id("char", mal_id)
        buttons = [[InlineKeyboardButton("More Info!", url = mal_url)]]
        await EMILIA.send_message(chat_id = message.chat.id, text = text, parse_mode = "markdown", reply_markup = InlineKeyboardMarkup(buttons))
    except Exception as e:
        await EMILIA.send_message(chat_id = message.chat.id, text = e)