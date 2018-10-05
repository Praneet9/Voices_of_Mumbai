from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

def echo(bot, update):
    update.message.reply_text(update.message.text)

def main():
    TOKEN = open('./api_key/api.txt').read()

    updater = Updater(TOKEN)

    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.text, echo))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()