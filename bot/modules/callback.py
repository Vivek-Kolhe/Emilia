import os
import shutil
from bot import EMILIA
from .nhentai import _download, nhentai_data
from .mal import data_from_id
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, InputMediaDocument

@EMILIA.on_callback_query()
async def _callback(client, CallbackQuery):
    query = CallbackQuery.data.split()
    try:
        if query[0] == "anime":
            text, mal_url, trailer = data_from_id(query[0], query[-1])
            if trailer:
                buttons = [
                            [InlineKeyboardButton("More Info!", url = mal_url), InlineKeyboardButton("Watch Trailer!", url = trailer)]
                        ]
            else:
                buttons = [
                            [InlineKeyboardButton("More Info!", url = mal_url)]
                        ]
            await CallbackQuery.edit_message_text(text = text, reply_markup = InlineKeyboardMarkup(buttons))
        elif query[0] == "manga" or query[0] == "char":
            text, mal_url = data_from_id(query[0], query[-1])
            buttons = [
                        [InlineKeyboardButton("More Info!", url = mal_url)]
                    ]
            await CallbackQuery.edit_message_text(text = text, reply_markup = InlineKeyboardMarkup(buttons))
        
        elif query[0] == "download":
            title, num_pages, artist, lang, tags, page_links = await nhentai_data(query[-1])
            cwd = os.getcwd()
            new_dir = query[-1]
            dl_path = os.path.join(cwd, new_dir)
            os.mkdir(dl_path)
            outfile_path = os.path.join(dl_path, f"{new_dir}.pdf")
            await _download(query[-1], dl_path, outfile_path)
            print()
            text = f"**{title}**\n\n**Language:** {', '.join(lang)}\n**Artist:** {', '.join(artist)}\n**Pages:** {num_pages}\n\n**Tags:** {', '.join(tags)}"
            await CallbackQuery.edit_message_media(InputMediaDocument(outfile_path, caption = text))
            shutil.rmtree(dl_path)
    except Exception as e:
        await CallbackQuery.edit_message_text(text = f"**Error:**\n{e}")
