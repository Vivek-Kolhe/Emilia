from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
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
            title_jap = data["title_japanese"]
            _type = data["type"]
            volumes = data["volumes"]
            chapters = data["chapters"]
            status = data["status"]
            score = data["score"]
            description = text_shortner.make_short(data["synopsis"], thumb, mal_url)
            genre = [item["name"] for item in data["genres"]]
            authors = [item["name"] for item in data["authors"]]

            text = f"**{title} ({title_jap})**\n\n**MAL ID:** `{_id}`\n**Type:** `{_type}`\n**Volumes:** `{volumes}`\n**Chapters:** `{chapters}`\n**Authors:** `{'; '.join(authors)}`\n**Status:** `{status}`\n**Score:** `{score}` ⭐\n**Genre:** `{', '.join(genre)}`\n\n**Description:** {description}"
            return text, mal_url
        
        elif category == "anime":
            data = jikan.anime(mal_id)
            _id = mal_id
            mal_url = data["url"]
            thumb = data["image_url"]
            trailer = data["trailer_url"]
            title = data["title"]
            title_jap = data["title_japanese"]
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

            text = f"**{title} ({title_jap})**\n\n**MAL ID:** `{_id}`\n**Type:** `{_type}`\n**Episodes:** `{episodes}`\n**Duration:** `{duration}`\n**Premiered:** `{premiered}`\n**Status:** `{status}`\n**Rating:** `{rating}`\n**Score:** `{score}` ⭐\n**Genre:** `{', '.join(genre)}`\n**Studio:** `{', '.join(studios)}`\n\n**Description:** {description}"
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
            description = text_shortner.make_short(data["about"], thumb, mal_url).replace("\r", "").replace("\\n", "").replace("\n\n\n", "\n").replace("\n\n", "\n")
            anime = [item["name"] for item in data["animeography"]]

            text = f"**MAL ID:** `{_id}`\n**Name:** `{name}`\n**Nicknames:** `{nicknames}`\n**Anime:** `{', '.join(anime)}`\n\n**About:** {description}"
            return text, mal_url
    except Exception as e:
        return e

@EMILIA.on_message(filters.command(["mal_id"], prefixes = "/") & ~filters.edited)
async def mal(client, message):
    query = message.text.split(maxsplit = 1)
    if len(query) < 2:
        text = "No ID found!\nExample:\n**/mal_id 1234566**"
        await EMILIA.send_message(chat_id = message.chat.id, text = text, parse_mode = "markdown")
        return

    buttons = [
                [InlineKeyboardButton("Anime", f"anime {query[-1]}"), InlineKeyboardButton("Manga", f"manga {query[-1]}"), InlineKeyboardButton("Character", f"char {query[-1]}")]
              ]
    text = "What are you looking for?"
    await EMILIA.send_message(chat_id = message.chat.id, text = text, reply_markup = InlineKeyboardMarkup(buttons))
