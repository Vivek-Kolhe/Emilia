def make_short(description, thumb, mal_url):
    if len(description) < 750:
        description += f"\n[R]({thumb})[ead more!]({mal_url})"
        return description
    else:
        description = description[:751]
        description += f"[...]({thumb})\n[Read more!]({mal_url})"
        return description
