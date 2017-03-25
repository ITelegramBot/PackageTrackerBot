from markupsafe import Markup, escape
import telebot
import api
import db

DATABASE = db.getDb("bot.db")


def getTracker(bot, logger):
    """
    Get the tracker
    
    :type bot: telebot.TeleBot
    :param bot: The TeleBot
    :return: the Package Tracker 
    """

    class PackagerTracker(object):
        def __init__(self):
            pass

        @staticmethod
        @bot.message_handler(commands=['start'])
        def send_welcome(message):
            logger.info(str(message.chat.id) + " is start")
            bot.reply_to(message, "Hi")

        @staticmethod
        @bot.message_handler(commands=['new'])
        def create_query(message):
            if len(str(message.text).split(" ")[1:]) == 0:
                bot.send_message(message.chat.id, "Error: Please input a PackageId")
                return

            packageID = str(escape(str(message.text).split(" ")[1]))
            packageProvider = ""
            packageName = "Package %s" % str(packageID)[:4]
            packageStatus = 0

            if len(str(message.text).split(" ")[1:]) >= 2:
                packageName = str(escape(str(message.text).split(" ")[2]))

            if len(str(message.text).split(" ")[1:]) == 3:
                packageProvider = str(escape(str(message.text).split(" ")[3]))

            try:
                packageProvider = api.TrackerApi.getPackageProvider(packageID)
            except ValueError:
                if packageProvider == "":
                    bot.send_message(message.chat.id, "Error: Package not found, please check or add force.")
                    return

            lastDate = ""
            try:
                data = api.TrackerApi.getPackageInformation(packageID, packageProvider)
                if data["data"]:
                    lastDate = data["data"][0]["time"]
                    packageStatus = data["status"]
            except ValueError:
                pass
            try:
                DATABASE.newPackage(message.chat.id, packageID, packageProvider, lastDate, packageName, packageStatus)
            except ValueError:
                bot.send_message(message.chat.id, "Can't add same package!")
                return
            logger.info("Starting a new package: " + packageID)
            bot.send_message(message.chat.id, "Your package \'%s[%s]\' is saved" % (packageName, packageProvider))

        @staticmethod
        @bot.message_handler(commands=['list'])
        def list_package(message):
            messages = ""
            for package in DATABASE.getUserAll(message.chat.id):
                messages += "\n" + package[5] + " - " + package[0] + " - " + api.getStatusFromCode(package[1]) +\
                            " - " + api.TrackerApi.getLastMessage(package[0], package[3])
            bot.send_message(message.chat.id, "Your Packages:" + messages)

        @staticmethod
        @bot.message_handler(commands=['remove'])
        def remove_package(message):
            if len(str(message.text).split(" ")[1:]) == 0:
                bot.send_message(message.chat.id, "Error: Please input a PackageId")
                return

            packageID = str(escape(str(message.text).split(" ")[1]))

            DATABASE.removePackage(message.chat.id, packageID)

            logger.info("Removed a package: " + packageID)

            bot.send_message(message.chat.id, "Removed package: " + packageID)

        @staticmethod
        @bot.message_handler(commands=['fetch'])
        def fetch_package(message):
            if len(str(message.text).split(" ")[1:]) == 0:
                bot.send_message(message.chat.id, "Error: Please input a PackageId")
                return

            packageID = str(escape(str(message.text).split(" ")[1]))

            logger.info("Fetched a package: " + packageID)
            info = api.TrackerApi.getPackageInformation(packageID)
            messages = ""
            if info["data"]:
                for item in info["data"]:
                    message += "\n" + item["data"] + " - " + item["time"]
                bot.send_message(message.chat.id, "Fetched Package: " + packageID + messages)
            else:
                bot.send_message(message.chat.id, "Error: Package not found")
            
    return PackagerTracker
