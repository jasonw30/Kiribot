import kiribot
import configparser
import pathlib

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read(pathlib.Path("configuration.ini"))
    bot_token = config.get('Discord-Bot', 'BotToken')
    bot = kiribot.KiriBot(bot_token)
