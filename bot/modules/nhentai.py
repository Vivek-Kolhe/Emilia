import requests
import wget
from bs4 import BeautifulSoup

def nhentai_data(_id):
    url = f"https://nhentai.net/g/{_id}/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "lxml")

    title = soup.find("h1", class_ = "title").text
    section_tags = soup.find_all(id = "tags")
    divs = section_tags[0].find_all("div")
    tags = divs[2].find_all("span", class_ = "name")
    tags = [item.text for item in tags]
    artist = divs[3].find("span", class_ = "name").text
    pages = divs[7].find("span", class_ = "name").text

    some_id = soup.find("div", class_ = "thumb-container").find("noscript").find("img")["src"].split("/")[-2]
    BASE_IMG_URL = "https://i.nhentai.net/galleries/{}/".format(some_id)

    for i in range(int(pages)):
        url = BASE_IMG_URL + f"{i+1}.jpg"
        wget.download(url, "E://test")
    return title, tags, artist, pages

title, tags, artist, pages = nhentai_data(339813)
print(title)
print(", ".join(tags))
print(artist)
print(pages)