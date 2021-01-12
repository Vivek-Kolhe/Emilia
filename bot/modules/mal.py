from jikanpy import Jikan
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from bot.utils import text_shortner
from bot import EMILIA

jikan = Jikan()

def data_from_id(category, mal_id):                             # category: anime or manga
    try:
        if category == "manga_id":
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
            description = text_shortner.make_short(data["synopsis"], mal_url)
            genre = [item["name"] for item in data["genres"]]
            authors = [item["name"] for item in data["authors"]]

            text = f"**MAL ID:** `{_id}`\n**Title:** `{title}`\n**JP Title:** `{title_jap}`\n**ENG Title:** `{title_eng}`\n**Type:** `{_type}`\n**Volumes:** `{volumes}`\n**Chapters:** `{chapters}`\n**Authors:** `{'; '.join(authors)}`\n**Status:** `{status}`\n**Score:** `{score}` ⭐\n**Genre:** `{', '.join(genre)}`\n\n**Description:** {description}"
            return text, mal_url, thumb
        
        elif category == "anime_id":
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
            description = text_shortner.make_short(data["synopsis"], mal_url)
            genre = [item["name"] for item in data["genres"]]
            studios = [item["name"] for item in data["studios"]]

            text = f"**MAL ID:** `{_id}`\n**Title:** `{title}`\n**JP Title:** `{title_jap}`\n**ENG Title:** `{title_eng}`\n**Type:** `{_type}`\n**Episodes:** `{episodes}`\n**Duration:** `{duration}`\n**Premiered:** `{premiered}`\n**Status:** `{status}`\n**Rating:** `{rating}`\n**Score:** `{score}` ⭐\n**Genre:** `{', '.join(genre)}`\n**Studio:** `{', '.join(studios)}`\n\n**Description:** {description}"
            return text, mal_url, thumb, trailer
        
        elif category == "char_id":
            data = jikan.character(mal_id)
            _id = mal_id
            mal_url = data["url"]
            name = data["name"]
            if data["nicknames"]:
                nicknames = ", ".join(data["nicknames"])
            else:
                nicknames = None
            description = text_shortner.make_short(data["about"], mal_url).replace("\\n", "\n").replace("\n", "")
            thumb = data["image_url"]
            anime = [item["name"] for item in data["animeography"]]

            text = f"**MAL ID:** `{_id}`\n**Name:** `{name}`\n**Nicknames:** `{nicknames}`\n**Anime:** `{', '.join(anime)}`\n\n**About:** {description}"
            return text, mal_url, thumb
    except Exception as e:
        return e

@EMILIA.on_message(filters.command(["anime_id"], prefixes = "/") & ~filters.edited)
async def get_anime_via_id(client, message):
    query = message.text.split()
    if len(query) < 2:
        text = "No ID found.\nExample:\n<b>/anime_id 2167</b>"
        await EMILIA.send_message(chat_id = message.chat.id, text = text, parse_mode = "html")
        return
    try:
        category, mal_id = query[0][1:], query[-1]
        caption, mal_url, thumb, trailer = data_from_id(category, mal_id)
        if trailer:
            buttons = [
                        [InlineKeyboardButton("More Info!", url = mal_url), InlineKeyboardButton("Watch Trailer!", url = trailer)]
                        ]
        else:
            buttons = [
                        [InlineKeyboardButton("More Info!", url = mal_url)]
                        ]
        await EMILIA.send_photo(chat_id = message.chat.id, photo = thumb, caption = caption, parse_mode = "markdown", reply_markup = InlineKeyboardMarkup(buttons))
    except Exception as e:
        await EMILIA.send_message(chat_id = message.chat.id, text = e)

@EMILIA.on_message(filters.command(["manga_id"], prefixes = "/") & ~filters.edited)
async def get_manga_via_id(client, message):
    query = message.text.split()
    if len(query) < 2:
        text = "No ID found.\nExample:\n<b>/manga_id 2167</b>"
        await EMILIA.send_message(chat_id = message.chat.id, text = text, parse_mode = "html")
        return
    try:
        category, mal_id = query[0][1:], query[-1]
        caption, mal_url, thumb = data_from_id(category, mal_id)
        buttons = [[InlineKeyboardButton("More Info!", url = mal_url)]]
        await EMILIA.send_photo(chat_id = message.chat.id, photo = thumb, caption = caption, parse_mode = "markdown", reply_markup = InlineKeyboardMarkup(buttons))
    except Exception as e:
        await EMILIA.send_message(chat_id = message.chat.id, text = e)

@EMILIA.on_message(filters.command(["char_id"], prefixes = "/") & ~filters.edited)
async def get_char_via_id(client, message):
    query = message.text.split()
    if len(query) < 2:
        text = "No ID found.\nExample:\n<b>/char_id 2167</b>"
        await EMILIA.send_message(chat_id = message.chat.id, text = text, parse_mode = "html")
        return
    try:
        category, mal_id = query[0][1:], query[-1]
        caption, mal_url, thumb = data_from_id(category, mal_id)
        buttons = [[InlineKeyboardButton("More Info!", url = mal_url)]]
        await EMILIA.send_photo(chat_id = message.chat.id, photo = thumb, caption = caption, parse_mode = "markdown", reply_markup = InlineKeyboardMarkup(buttons))
    except Exception as e:
        await EMILIA.send_message(chat_id = message.chat.id, text = e)

@EMILIA.on_message(filters.command(["schedule"], prefixes = "/") & ~filters.edited)
async def schedule(client, message):
    query = message.text.split()
    if len(query) < 2:
        text = "You forgot to mention day!\nExample:\n**/schedule monday**"
        await EMILIA.send_message(chat_id = message.chat.id, text = text, parse_mode = "markdown")
        return
    try:
        data = jikan.schedule(day = query[-1].lower())
        data = data[query[-1].lower()]
        SCHEDULE_TEXT = f"**Schedule for {query[-1].title()}**\n\n"
        
        for i in range(len(data)):
            title = data[i]["title"]
            time = data[i]["airing_start"].split("T")[-1][:8] + " UTC"
            SCHEDULE_TEXT += f"● `{title}` | `{time}`\n"
        SCHEDULE_TEXT += "\n**Source:** MAL"

        await EMILIA.send_message(chat_id = message.chat.id, text = SCHEDULE_TEXT, parse_mode = "markdown")
    
    except Exception as e:
        await EMILIA.send_message(chat_id = message.chat.id, text = e)
