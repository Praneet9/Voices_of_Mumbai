import telegram
import pprint


TOKEN = open('./api_key/api.txt').read()
bot = telegram.Bot(token=TOKEN)
# updates = bot.get_updates()
# print([u.message.photo for u in updates if u.message.photo])
# i = 0
# for update in updates:
#     if update.message.photo:
#         print(update.message.photo[-1].get_file())
#     i += 1

upd = bot.get_updates()[-1].to_dict()
user_id = upd.get('message').get('from').get('id')
first_name = upd.get('message').get('from').get('first_name')
last_name = upd.get('message').get('from').get('last_name')
msg = upd.get('message').get('text')
print(msg)