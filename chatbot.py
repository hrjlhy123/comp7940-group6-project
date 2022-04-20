# The code was done by HAO Ruojie (21415315), ZHAO Zimeng (21458839), and Khem LIMBU (21470634).
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler

import configparser
import logging
import redis
import os
import re

# Database
import mysql.connector

db_user = os.environ['db_user']
db_psw = os.environ['db_psw']
db_host = os.environ['db_host']
db_port = os.environ['db_port']
db_db = os.environ['db_db']

def main():
    # Load token and create an Updater
    updater = Updater(token=(os.environ['ACCESS_TOKEN']), use_context=True)
    dispatcher = updater.dispatcher
    
    # Set logging module to know when and why things do not work as expected
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    
    # Register a dispatcher to handle message: here we register an echo dispatcher
    echo_handler = MessageHandler(Filters.text & (~Filters.command) & (Filters.regex(re.compile(r'hi', re.IGNORECASE)) | Filters.regex(re.compile(r'hello', re.IGNORECASE))), echo)
    dispatcher.add_handler(echo_handler)

    # Register a dispatcher to handle message: here we register an echo dispatcher
    movie_handler = MessageHandler(Filters.text & (~Filters.command) & (Filters.regex(re.compile(r'movie', re.IGNORECASE)) | Filters.regex(re.compile(r'film', re.IGNORECASE)) | Filters.regex(re.compile(r'cinematic', re.IGNORECASE)) | Filters.regex(re.compile(r'program', re.IGNORECASE)) | Filters.regex(re.compile(r'show', re.IGNORECASE)) | Filters.regex(re.compile(r'episode', re.IGNORECASE)) | Filters.regex(re.compile(r'segment', re.IGNORECASE))), movie_command)
    dispatcher.add_handler(movie_handler)

    # On different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("hello", hello_command))
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
    print("context.callback_query.data: " + update.callback_query.data)
    query = ("SELECT Title, Content FROM MOVIES WHERE Content ='" + update.callback_query.data +"'")
    cursor.execute(query)
    print("Works well!query")
    for (i) in cursor:
        update.callback_query.message.edit_text("I give you some idea, you can watch the movie: <{}>".format(i[0]))
        break
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
        query = ("SELECT Title, Content FROM MOVIES " 
        "WHERE Content ='" + context.args[0]+ "'")
        cursor.execute(query)
        for (i) in cursor:
            update.message.reply_text("Movie: {}".format(i[0]))
        cursor.close()
        cnx.close()
    except (IndexError, ValueError):
        # User: Give me horor movie/ Shows me horor movie. User: /movie_search horor
        update.message.reply_text('Usage: /movie_search <keyword>')

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
        cursor = cnx.cursor()
        print("cursor done")
        insertSql = ("INSERT INTO MOVIES (Title, Content) VALUES ('" + title + "', '" + content + "')")
        print(insertSql)
        try:
            cursor.execute(insertSql)
            cnx.commit()
            print("execute")
            for (i) in cursor:
                update.message.reply_text("Movie has been successful added!")
                update.message.reply_text("Title: {}, Content: {}".format(i[0], i[1]))
                print("Title: {}, Content: {}".format(i[0], i[1]))
        except:
            cnx.rollback()
        print("Works well!end")
    except (IndexError, ValueError, DatabaseError):
        # User: Add a movie. User: /movie_add movieTitle_moviecontent
        update.message.reply_text('Usage: /movie_add <keyword>')
    finally:
        if cursor:
            cursor.close()
        cnx.close()

if __name__ == '__main__':
    main()
