import aiohttp
from bot import EMILIA
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

async def nhentai_data(_id):
    url = f"https://nhentai.net/api/gallery/{_id}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()

            title = data["title"]["english"]
            media_id = data["media_id"]
            pages = data["images"]["pages"]
            num_pages = data["num_pages"]
            all_tags = data["tags"]
            lang, artist, tags = [], [], []

            for tag in all_tags:
                if tag["type"] == "tag":
                    tags.append(f"#{tag['name'].replace(' ', '_').replace('-', '_')}")
                elif tag["type"] == "language":
                    lang.append(tag["name"].title())
                elif tag["type"] == "artist":
                    artist.append(tag["name"].title()) 

            BASE_PAGE_IMG = f"https://i.nhentai.net/galleries/{media_id}/"
            page_links = []
            img_extensions = {
                                "j" : "jpg",
                                "p" : "png",
                                "g" : "gif"
                             }
            
            for i in range(num_pages):
                temp_ext = pages[i]["t"]
                file_url = BASE_PAGE_IMG + f"{i+1}.{img_extensions[temp_ext]}"
                page_links.append(file_url)
            
            return title, num_pages, artist, lang, tags, page_links

@EMILIA.on_message(filters.command(["nhentai"], prefixes = "/") & ~filters.edited)
async def nhentai(client, message):
    query = message.text.split()
    title, num_pages, artist, lang, tags, page_links = await nhentai_data(query[-1])

    buttons = [
                [
                    InlineKeyboardButton("Instant Read?", url = "https://nhentai.net"),
                    InlineKeyboardButton("Download", callback_data = "some")
                ]
              ]

    text = f"**{title}**\n\n**Language:** {', '.join(lang)}\n**Artist:** {', '.join(artist)}\n**Pages:** {num_pages}\n\n**Tags:** {', '.join(tags)}"
    await EMILIA.send_photo(chat_id = message.chat.id, photo = page_links[0], caption = text, reply_markup = InlineKeyboardMarkup(buttons))
