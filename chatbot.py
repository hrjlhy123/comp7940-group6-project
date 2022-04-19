from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler

import configparser
import logging
import redis
import os
import re
# database
import mysql.connector

# cnx = mysql.connector.connect(user='doadmin', password='AVNS_IZcLYrdx6q27Ry2',
#                               host='db-mysql-sgp1-31144-do-user-11210025-0.b.db.ondigitalocean.com',
#                               port='25060'
#                               database='defaultdb')
# cnx.close()

# import configparser

global redis1

#global db_user = os.environ['ACCESS_TOKEN']
db_user = 'doadmin'
db_psw = 'AVNS_IZcLYrdx6q27Ry2'
db_host = 'db-mysql-sgp1-31144-do-user-11210025-0.b.db.ondigitalocean.com'
db_port = '25060'
db_db = 'defaultdb'

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
    echo_handler = MessageHandler(Filters.text & (~Filters.command) & (Filters.regex(re.compile(r'hi', re.IGNORECASE)) | Filters.regex(re.compile(r'hello', re.IGNORECASE))), echo)
    dispatcher.add_handler(echo_handler)

    # register a dispatcher to handle message: here we register an echo dispatcher
    movie_handler = MessageHandler(Filters.text & (~Filters.command) & (Filters.regex(re.compile(r'movie', re.IGNORECASE)) | Filters.regex(re.compile(r'film', re.IGNORECASE)) | Filters.regex(re.compile(r'cinematic', re.IGNORECASE)) | Filters.regex(re.compile(r'program', re.IGNORECASE)) | Filters.regex(re.compile(r'show', re.IGNORECASE)) | Filters.regex(re.compile(r'episode', re.IGNORECASE)) | Filters.regex(re.compile(r'segment', re.IGNORECASE))), movie_command)
    dispatcher.add_handler(movie_handler)

    # on different commands - answer in Telegram
    # dispatcher.add_handler(CommandHandler("add", add))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("hello", hello_command))
    # /movie Horror -> Scary Movie
    dispatcher.add_handler(CommandHandler("movie", movie_command))
    dispatcher.add_handler(CallbackQueryHandler(movie_reply_command))
    dispatcher.add_handler(CommandHandler("movie_search", movie_search_command))
    dispatcher.add_handler(CommandHandler("movie_add", movie_add_command))

    dispatcher.add_handler(CommandHandler("cooking", cooking_command))
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
# def add(update: Update, context: CallbackContext) -> None:
#     """Send a message when the command /add is issued."""
#     try: 
#         global redis1
#         logging.info(context.args[0])
#         msg = context.args[0]   # /add keyword <-- this should store the keyword
#         redis1.incr(msg)
#         update.message.reply_text('You have said ' + msg +  ' for ' + redis1.get(msg).decode('UTF-8') + ' times.')
#     except (IndexError, ValueError):
#         update.message.reply_text('Usage: /add <keyword>')

def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Helping you helping you.')

def hello_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /hello is issued."""
    try: 
        logging.info(context.args[0])
        msg = context.args[0]
        update.message.reply_text('Good day, ' + msg + '!')
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /hello <keyword>')

def cooking_command(update: Update, context: CallbackContext) -> None:
    try: 
        msg = context.args[0]
        logging.info(msg)
        cnx = mysql.connector.connect(user=db_user, 
                            password=db_psw,
                            host=db_host,
                            port=db_port,
                            database=db_db)
        cursor = cnx.cursor()
        query = ("SELECT Address FROM COOKING WHERE Name like '%" + msg +"%';")
        print("Works well!query")
        cursor.execute(query)
        for (i) in cursor:
            update.message.reply_text("COOKING: {}".format(i[0]))
            print("COOKING: {}".format(i[0]))
        cursor.close()
        cnx.close()
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /COOKING <keyword>')

def movie_command(update, context):
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    update.message.reply_text('Which type of movie do you want to watch?',
    reply_markup = InlineKeyboardMarkup([[
            InlineKeyboardButton(text = "Comedy", callback_data = "Comedy"), 
            InlineKeyboardButton(text = "Romance", callback_data = "Romance"),
            InlineKeyboardButton(text = "Horror", callback_data = "Horror"),
            InlineKeyboardButton(text = "Plot", callback_data = "Plot")
        ]]))

def movie_reply_command(update, context):
    cnx = mysql.connector.connect(user=db_user, 
                        password=db_psw,
                        host=db_host,
                        port=db_port,
                        database=db_db)
    cursor = cnx.cursor()
    # print("update: " + update)
    print("context.callback_query.data: " + update.callback_query.data)
    query = ("SELECT Title, Content FROM MOVIES WHERE Content ='" + update.callback_query.data +"'")
    cursor.execute(query)
    print("Works well!query")
    update.callback_query.message.edit_text("I give you some idea, you can watch the movie: <{}>".format(cursor[0]))
    print("Works well!reply")
    cursor.close()
    cnx.close()

def movie_search_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /movie_search is issued."""
    try:
        logging.info(context.args[0])
        cnx = mysql.connector.connect(user=db_user, 
                            password=db_psw,
                            host=db_host,
                            port=db_port,
                            database=db_db)
        cursor = cnx.cursor()
        # print("Works well!1")
        query = ("SELECT Title, Content FROM MOVIES " 
        "WHERE Content ='" + context.args[0]+ "'")
        # print("Works well!2")
        cursor.execute(query)
        # print("Works well!3")
        for (i) in cursor:
            update.message.reply_text("Movie: {}".format(i[0]))
            # print("Works well!for")
        cursor.close()
        cnx.close()
        # print("Works well!end")
    except (IndexError, ValueError):
        # User: Give me horor movie/ Shows me horor movie. User: /movie horor
        update.message.reply_text('Usage: /movie <keyword>')

def movie_add_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /movie_add is issued."""
    try:
        title = context.args[0].split("_")[0]
        content = context.args[0].split("_")[1]
        logging.info("title: " + title + ", content: " + content)
        cnx = mysql.connector.connect(user=db_user, 
                            password=db_psw,
                            host=db_host,
                            port=db_port,
                            database=db_db)
        conn.enter_transaction_management()
        cursor = cnx.cursor()
        print("cursor done")
        insertSql = ("INSERT INTO MOVIES (Title, Content) VALUES ('" + title + "', '" + content + "')")
        print(insertSql)
        cursor.execute(insertSql)
        cursor.commit()
        print("execute")
        for (i) in cursor:
            update.message.reply_text("Movie has been successful added!")
            update.message.reply_text("Title: {}, Content: {}".format(i[0], i[1]))
            print("Title: {}, Content: {}".format(i[0], i[1]))
        #cursor.close()
        #cnx.close()
        print("Works well!end")
    except (IndexError, ValueError, DatabaseError):
        # User: Give me horor movie/ Shows me horor movie. User: /movie horor
        update.message.reply_text('Usage: /movie <keyword>')
    finally:
        if cursor:
            cursor.close()
        conn.leave_transaction_management()

# The code was done by Ruojie Hao (Student ID: 21415315).

if __name__ == '__main__':
    main()


