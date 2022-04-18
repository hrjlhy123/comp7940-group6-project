from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

import configparser
import logging
import redis
import os
# database
import mysql.connector

# cnx = mysql.connector.connect(user='doadmin', password='AVNS_IZcLYrdx6q27Ry2',
#                               host='db-mysql-sgp1-31144-do-user-11210025-0.b.db.ondigitalocean.com',
#                               port='25060'
#                               database='defaultdb')
# cnx.close()

# import configparser

global redis1

def main():
    # Load your token and create an Updater for your Bot
    
    # config = configparser.ConfigParser()
    # config.read('config.ini')
    updater = Updater(token=(os.environ['ACCESS_TOKEN']), use_context=True)
    dispatcher = updater.dispatcher

    global redis1
    redis1 = redis.Redis(host=(os.environ['HOST']), password=(os.environ['PASSWORD']), port=(os.environ['REDISPORT']))

    # You can set this logging module, so you will know when and why things do not work as expected
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    
    # register a dispatcher to handle message: here we register an echo dispatcher
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(echo_handler)

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("add", add))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("hello", hello_command))
    dispatcher.add_handler(CommandHandler("movie", movie_command))
    # To start the bot:
    updater.start_polling()
    updater.idle()


def echo(update, context):
    reply_message = update.message.text.upper()
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    context.bot.send_message(chat_id=update.effective_chat.id, text= reply_message)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def add(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /add is issued."""
    try: 
        global redis1
        logging.info(context.args[0])
        msg = context.args[0]   # /add keyword <-- this should store the keyword
        redis1.incr(msg)
        update.message.reply_text('You have said ' + msg +  ' for ' + redis1.get(msg).decode('UTF-8') + ' times.')
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /add <keyword>')

def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Helping you helping you.')

def hello_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /hello is issued."""
    try: 
        logging.info(context.args[0])
        msg = context.args[0]   # /hello keyword <-- this should store the keyword
        update.message.reply_text('Good day, ' + msg + '!')
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /hello <keyword>')

def movie_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /movie is issued."""
    try:
         cnx = mysql.connector.connect(user='doadmin', password='AVNS_IZcLYrdx6q27Ry2',
                              host='db-mysql-sgp1-31144-do-user-11210025-0.b.db.ondigitalocean.com',
                              port='25060',
                              database='defaultdb')
         cursor = cnx.cursor()
         print("Works well!1")
         query = ("SELECT Title, Content FROM MOVIES " 
         "WHERE ID =" + context.args[0])
         print("Works well!2")
         cursor.execute(query)
         print("Works well!3")
         for (title) in cursor:
             update.message.reply_text("Movie: {}, Content:{}".format(title))
             print("Works well!for")
         cursor.close()

         cnx.close()
         print("Works well!end")
    except (IndexError, ValueError):
        # User: Give me horor movie/ Shows me horor movie. User: /movie horor
        update.message.reply_text('Usage: /movie <keyword>')

# The code was done by Ruojie Hao (Student ID: 21415315).

if __name__ == '__main__':
    main()