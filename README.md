<!-- <img src="https://github.com/Vivek-Kolhe/Emilia/blob/main/132658.gif" alt="Emilia" width=5000 /> -->

# Emilia
A telegram bot to fetch anime, manga, character info from [MAL](https://myanimelist.net/).

## Dependencies
- JikanPy\
  ```pip3 install jikanpy```
  
- Pyrogram\
  ```pip3 install pyrogram```
  
***Or use:***\
```pip3 install -r requirements.txt```

## Available Commands
| **Commands** | **Description** |
|---|---|
| ```/start``` | Starts the bot. |
| ```/help``` | Help regarding the bot. |
| ```/anime <query>``` | Returns anime results from MAL. |
| ```/manga <query>``` | Returns manga results from MAL. |
| ```/character <query>``` | Returns characters results from MAL. |
| ```/mal_id <unique_id>``` | Returns results using ID. |
| ```/schedule <day>``` | Returns airing schedule. |

## Set Up
Clone and download the repository. Install above listed dependencies and put your *credentials* in ***config.py***.\
Run the bot using ```python3 -m bot```.

## Deploying on Heroku
- Clone and download the repository.
- Get your telegram **api_id** and **api_hash** from [here](https://my.telegram.org/) and put them in *config.py*.
- Get **bot_token** from [BotFather](https://t.me/BotFather) and put them in *config.py*.
- Download **HerokuCLI** and create an app from the dashboard.
- Navigate inside the directory where all the repo files are present and run the following commands.
    ```
    heroku login
    heroku git:remote -a <appname>
    git init
    git add .
    git commit -am "deploying"
    git push heroku master
    ```
***Note:*** Pass the **api_id** as an integer.
