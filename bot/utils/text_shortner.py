def make_short(description, mal_url):
    if len(description) < 650:
        return description
    else:
        description = description[:651]
        description += f"...\n[Read more!]({mal_url})"
        return description
