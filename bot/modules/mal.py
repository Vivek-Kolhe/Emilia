from jikanpy import Jikan
from pyrogram import filters
from bot.utils import text_shortner
from bot import EMILIA

jikan = Jikan()

def data_from_id(mal_id):
    data = jikan.anime(mal_id)
    try:
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

        text = f"**Title:** `{title}`\n**JP Title:** `{title_jap}`\n**ENG Title:** `{title_eng}`\n**Type:** `{_type}`\n**Episodes:** `{episodes}`\n**Duration:** `{duration}`\n**Premiered:** `{premiered}`\n**Status:** `{status}`\n**Rating:** `{rating}`\n**Score:** `{score}`⭐\n**Genre:** `{', '.join(genre)}`\n**Studios:** `{', '.join(studios)}`\n\n**Description:** {description}"

        return text, mal_url, thumb, trailer
    except Exception as e:
        return e

@EMILIA.on_message(filters.command(["mal_id"], prefixes = "/") & ~filters.edited)
def get_via_id(client, message):
    mal_id = message.text.split()[-1]
    try:
        caption, mal_url, thumb, trailer = data_from_id(mal_id)
        EMILIA.send_photo(chat_id = message.chat.id, photo = thumb, caption = caption, parse_mode = "markdown")
    except Exception as e:
        EMILIA.send_message(chat_id = message.chat.id, text = e)