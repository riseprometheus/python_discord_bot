import discord_bot
import json
import os
import logging
from datetime import datetime
import sys
import getopt

enable_log_files = False


def init_environment():
    # todo: set up later to set log directory to specific location
    log_format = '{"level":"%(levelname)s", "time":"%(asctime)s", "text":"%(message)s"}'
    if enable_log_files:
        directory = "./logs"
        if not os.path.exists('./logs'):
            os.mkdir(directory)
        else:
            pass
        now = datetime.now()
        current_time_log = now.strftime("%H_%M_%S")
        log_format = '{"level":"%(levelname)s", "time":"%(asctime)s", "text":"%(message)s"}'
        logging.basicConfig(filename=f"{directory}/bot_log_{current_time_log}.log",
                            format=log_format, level=logging.INFO)
    else:
        logging.basicConfig(format=log_format, level=logging.INFO)

    logging.info(f"Starting bot")


def main():
    init_environment()
    bot = discord_bot.MyClient()

    if os.path.exists("token.json"):
        credentials = open("token.json")
        bot.run(json.load(credentials)["token"])
    else:
        logging.error('Can\'t locate token.json file')


if __name__ == '__main__':
    main()
