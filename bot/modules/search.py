from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from bot import EMILIA, jikan
from .mal import data_from_id

@EMILIA.on_message(filters.command(["anime"], prefixes = "/") & ~filters.edited)
async def get_anime(client, message):
    query = message.text.split(maxsplit = 1)
    if len(query) < 2:
        await EMILIA.send_message(chat_id = message.chat.id, text = "No search query found!\nExample:\n**/anime <anime_name>**", parse_mode = "markdown")
        return
    try:
        temp = jikan.search("anime", query[-1])
        buttons = []
        for i in range(5):
            try:
                temp_btn = [InlineKeyboardButton(temp["results"][i]["title"], f"anime {temp['results'][i]['mal_id']}")]
                buttons.append(temp_btn)
            except:
                break

        text = f"Search results for **{query[-1]}**:"
        await EMILIA.send_message(chat_id = message.chat.id, text = text, reply_markup = InlineKeyboardMarkup(buttons))
    except Exception as e:
        await EMILIA.send_message(chat_id = message.chat.id, text = f"**Error:**\n{e}")

@EMILIA.on_message(filters.command(["manga"], prefixes = "/") & ~filters.edited)
async def get_manga(client, message):
    query = message.text.split(maxsplit = 1)
    if len(query) < 2:
        await EMILIA.send_message(chat_id = message.chat.id, text = "No search query found!\nExample:\n**/manga <manga_name>**", parse_mode = "markdown")
        return
    try:
        temp = jikan.search("manga", query[-1])
        buttons = []
        for i in range(5):
            try:
                temp_btn = [InlineKeyboardButton(temp["results"][i]["title"], f"manga {temp['results'][i]['mal_id']}")]
                buttons.append(temp_btn)
            except:
                break

        text = f"Search results for **{query[-1]}**:"
        await EMILIA.send_message(chat_id = message.chat.id, text = text, reply_markup = InlineKeyboardMarkup(buttons))
    except Exception as e:
        await EMILIA.send_message(chat_id = message.chat.id, text = f"**Error:**\n{e}")

@EMILIA.on_message(filters.command(["character"], prefixes = "/") & ~filters.edited)
async def get_character(client, message):
    query = message.text.split(maxsplit = 1)
    if len(query) < 2:
        await EMILIA.send_message(chat_id = message.chat.id, text = "No search query found!\nExample:\n**/character <character_name>**", parse_mode = "markdown")
        return
    try:
        temp = jikan.search("character", query[-1])
        buttons = []
        for i in range(5):
            try:
                temp_btn = [InlineKeyboardButton(temp["results"][i]["name"], f"char {temp['results'][i]['mal_id']}")]
                buttons.append(temp_btn)
            except:
                break

        text = f"Search results for **{query[-1]}**:"
        await EMILIA.send_message(chat_id = message.chat.id, text = text, reply_markup = InlineKeyboardMarkup(buttons))
    except Exception as e:
        await EMILIA.send_message(chat_id = message.chat.id, text = f"**Error:**\n{e}")
