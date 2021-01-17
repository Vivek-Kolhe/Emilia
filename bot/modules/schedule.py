from bot import EMILIA, jikan
from pyrogram import filters

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