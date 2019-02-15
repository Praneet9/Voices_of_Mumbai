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

update = bot.get_updates()[-1]
# user_id = upd.get('message').get('from').get('id')
# first_name = upd.get('message').get('from').get('first_name')
# last_name = upd.get('message').get('from').get('last_name')
# msg = upd.get('message').get('text')
# print(upd)

location_keyboard = telegram.KeyboardButton(text="send_location", request_location=True)
contact_keyboard = telegram.KeyboardButton(text="send_contact", request_contact=True)
custom_keyboard = [[ location_keyboard, contact_keyboard ]]
reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
bot.send_message(chat_id=update.message.chat_id, 
                 text="Would you mind sharing your location and contact with me?", 
                 reply_markup=reply_markup)