def make_short(description, mal_url):
    if len(description) < 700:
        return description
    else:
        description = description[:701]
        description += f"...\n[Read more!]({mal_url})"
        return description