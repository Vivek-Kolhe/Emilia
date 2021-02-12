import aiohttp
import wget
from PIL import Image
from bot import EMILIA
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

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

async def _download(_id, dl_path, outfile_path):
    title, num_pages, artist, lang, tags, page_links = await nhentai_data(_id)
    imgs = []
    for i in range(1, int(num_pages) + 1):
        wget.download(page_links[i - 1], dl_path)
        suffix = page_links[i - 1].split(".")[-1]
        fname = f"{dl_path}//{i}.{suffix}"
        img = Image.open(fname)
        if img.mode == "RGBA":
            img = img.convert("RGB")
        imgs.append(img)
    
    imgs[0].save(outfile_path, save_all = True, quality = 100, append_images = imgs[1:])

@EMILIA.on_message(filters.command(["nhentai"], prefixes = "/") & ~filters.edited)
async def nhentai(client, message):
    query = message.text.split(maxsplit = 1)
    if len(query) < 2:
        await EMILIA.send_message(chat_id = message.chat.id, text = "No nhentai ID found!\nExample:\n**/nhentai 339813**")
        return
    
    try:
        title, num_pages, artist, lang, tags, page_links = await nhentai_data(query[-1])
        buttons = [
                    [
                        InlineKeyboardButton("Download", callback_data = f"download {query[-1]}")
                    ]
                ]
        text = f"**{title}**\n\n**Language:** {', '.join(lang)}\n**Artist:** {', '.join(artist)}\n**Pages:** {num_pages}\n\n**Tags:** {', '.join(tags)}"
        await EMILIA.send_photo(chat_id = message.chat.id, photo = page_links[0], caption = text, reply_markup = InlineKeyboardMarkup(buttons))
    except Exception as e:
        await EMILIA.send_message(chat_id = message.chat.id, text = f"**Error:**\n{e}")
