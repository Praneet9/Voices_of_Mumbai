from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)

def echo(bot, update):
    update.message.reply_text(update.message.text)

def main():
    TOKEN = open('./api_key/api.txt').read()

    updater = Updater(TOKEN)

    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)


    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()