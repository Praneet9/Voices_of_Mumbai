import telegram


TOKEN = open('./api_key/api.txt').read()
bot = telegram.Bot(token=TOKEN)
updates = bot.get_updates()
print([u.message.photo for u in updates if u.message.photo])
i = 0
for update in updates:
    if update.message.photo:
        print(update.message.photo[-1].get_file())
    i += 1