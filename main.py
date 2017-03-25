import logging
import telebot
import timer
import bot
import os

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logging.info("Begin start server.")
tgBot = telebot.TeleBot(os.getenv("BOT_ID", ""))

bot.getTracker(tgBot, logging)()

timer.getTimer(tgBot, logging)("Timer").start()

logging.info("Start polling")
while True:
    try:
        tgBot.polling()
    except Exception as e:
        logging.error(e.message)

#
# import api
#
# print api.TrackerApi.getPackageInformation(3325607157191, "shentong")
