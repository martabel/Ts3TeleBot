# -*- coding: utf-8 -*-
import logging
from telegram import Updater
from subprocess import Popen
from subprocess import PIPE
from subprocess import call
import os
from tsInfoClient import getTSClients
from tsInfoClient import formatClients
import ts3TeleBotConfig

HELP = '''
Command list:
/help this help message
/hello hello message
/tsclients list of active teamspeak clientlist
/uptime runtime of the server
'''

#save PID
call(["echo "+str(os.getpid())+" > telegramBot.pid"], shell=True)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

updater = Updater(token=ts3TeleBotConfig.TELEGRAM_TOKEN)
dispatcher = updater.dispatcher

def hello(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Hello wurst koenig!!")

def uptime(bot, update):
    resUptime = str(Popen("uptime", shell=True, stdout=PIPE).stdout.read())
    bot.sendMessage(chat_id=update.message.chat_id, text=resUptime)

def listTSclients(bot, update):
    tsClients = getTSClients()
    if len(tsClients) > 0:
        fcList = formatClients(tsClients)
    else:
        fcList = "Nobody online :-("
    bot.sendMessage(chat_id=update.message.chat_id, text=fcList)

def helpMsg(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text=HELP)

dispatcher.addTelegramCommandHandler('hello', hello)
dispatcher.addTelegramCommandHandler('uptime', uptime)
dispatcher.addTelegramCommandHandler('tsclients', listTSclients)
dispatcher.addTelegramCommandHandler('help', helpMsg)

updater.start_polling()
