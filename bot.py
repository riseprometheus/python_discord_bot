import discord_bot
import json
import os
import logging
from datetime import datetime
import sys
import getopt


def init_environment(enable_log_files):
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
    enable_log_files = False
    argument_list = sys.argv[1:]
    options = "hmo:"
    long_options = ["log", "directory"]
    try:
        arguments, values = getopt.getopt(argument_list, options, long_options)
        for currentArgument, currentValue in arguments:
            if currentArgument in ("-l", "--log"):
                enable_log_files = True
            elif currentArgument in ("-d", "--directory"):
                pass
    except getopt.error as err:
        # output error, and return with an error code
        print(str(err))

    init_environment(enable_log_files)
    bot = discord_bot.MyClient()

    if os.path.exists("token.json"):
        credentials = open("token.json")
        bot.run(json.load(credentials)["token"])
    else:
        logging.error('Can\'t locate token.json file')


if __name__ == '__main__':
    main()
