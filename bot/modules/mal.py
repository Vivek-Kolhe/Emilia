from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from bot.utils import text_shortner
from bot import EMILIA, jikan

def data_from_id(category, mal_id):                             # category: anime or manga or character
    try:
        if category == "manga":
            data = jikan.manga(mal_id)
            _id = mal_id
            mal_url = data["url"]
            thumb = data["image_url"]
            title = data["title"]
            title_eng, title_jap = data["title_english"], data["title_japanese"]
            _type = data["type"]
            volumes = data["volumes"]
            chapters = data["chapters"]
            status = data["status"]
            score = data["score"]
            description = text_shortner.make_short(data["synopsis"], thumb, mal_url)
            genre = [item["name"] for item in data["genres"]]
            authors = [item["name"] for item in data["authors"]]

            text = f"**MAL ID:** `{_id}`\n**Title:** `{title}`\n**JP Title:** `{title_jap}`\n**ENG Title:** `{title_eng}`\n**Type:** `{_type}`\n**Volumes:** `{volumes}`\n**Chapters:** `{chapters}`\n**Authors:** `{'; '.join(authors)}`\n**Status:** `{status}`\n**Score:** `{score}` ⭐\n**Genre:** `{', '.join(genre)}`\n\n**Description:** {description}"
            return text, mal_url
        
        elif category == "anime":
            data = jikan.anime(mal_id)
            _id = mal_id
            mal_url = data["url"]
            thumb = data["image_url"]
            trailer = data["trailer_url"]
            title = data["title"]
            title_eng, title_jap = data["title_english"], data["title_japanese"]
            _type = data["type"]
            episodes = data["episodes"]
            duration = data["duration"]
            status = data["status"]
            rating = data["rating"]
            score = data["score"]
            premiered = data["premiered"]
            description = text_shortner.make_short(data["synopsis"], thumb, mal_url)
            genre = [item["name"] for item in data["genres"]]
            studios = [item["name"] for item in data["studios"]]

            text = f"**MAL ID:** `{_id}`\n**Title:** `{title}`\n**JP Title:** `{title_jap}`\n**ENG Title:** `{title_eng}`\n**Type:** `{_type}`\n**Episodes:** `{episodes}`\n**Duration:** `{duration}`\n**Premiered:** `{premiered}`\n**Status:** `{status}`\n**Rating:** `{rating}`\n**Score:** `{score}` ⭐\n**Genre:** `{', '.join(genre)}`\n**Studio:** `{', '.join(studios)}`\n\n**Description:** {description}"
            return text, mal_url, trailer
        
        elif category == "char":
            data = jikan.character(mal_id)
            _id = mal_id
            mal_url = data["url"]
            thumb = data["image_url"]
            name = data["name"]
            if data["nicknames"]:
                nicknames = ", ".join(data["nicknames"])
            else:
                nicknames = None
            description = text_shortner.make_short(data["about"], thumb, mal_url).replace("\\n", "\n").replace("\n", "")
            anime = [item["name"] for item in data["animeography"]]

            text = f"**MAL ID:** `{_id}`\n**Name:** `{name}`\n**Nicknames:** `{nicknames}`\n**Anime:** `{', '.join(anime)}`\n\n**About:** {description}"
            return text, mal_url
    except Exception as e:
        return e

@EMILIA.on_message(filters.command(["mal_id"], prefixes = "/") & ~filters.edited)
async def mal(client, message):
    query = message.text.split(maxsplit = 2)
    if len(query) < 3:
        text = "No ID or category found!\n**Format:** `/mal_id <category> <query>`"
        await EMILIA.send_message(chat_id = message.chat.id, text = text, parse_mode = "markdown")
        return
    if query[1] not in ["anime", "manga", "char"]:
        text = "Invalid category!\n**Categories:** anime, manga, char"
        await EMILIA.send_message(chat_id = message.chat.id, text = text, parse_mode = "markdown")
        return
    try:
        if query[1] == "anime":
            text, mal_url, trailer = data_from_id("anime", query[-1])
            if trailer:
                buttons = [
                            [InlineKeyboardButton("More Info!", url = mal_url), InlineKeyboardButton("Watch Trailer!", url = trailer)]
                          ]
            else:
                buttons = [
                            [InlineKeyboardButton("More Info!", url = mal_url)]
                          ]
            await EMILIA.send_message(chat_id = message.chat.id, text = text, parse_mode = "markdown", disable_web_page_preview = False, reply_markup = InlineKeyboardMarkup(buttons))
        
        elif query[1] == "manga":
            text, mal_url = data_from_id("manga", query[-1])
            buttons = [
                        [InlineKeyboardButton("More Info!", url = mal_url)]
                      ]
            await EMILIA.send_message(chat_id = message.chat.id, text = text, parse_mode = "markdown", disable_web_page_preview = False, reply_markup = InlineKeyboardMarkup(buttons))
        
        elif query[1] == "char":
            text, mal_url = data_from_id("char", query[-1])
            buttons = [
                        [InlineKeyboardButton("More Info!", url = mal_url)]
                      ]
            await EMILIA.send_message(chat_id = message.chat.id, text = text, parse_mode = "markdown", disable_web_page_preview = False, reply_markup = InlineKeyboardMarkup(buttons))
    except Exception as e:
        await EMILIA.send_message(chat_id = message.chat.id, text = f"Error:\n{e}")
