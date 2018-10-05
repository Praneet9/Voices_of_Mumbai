from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telegram
import copy
import logging
import json
import pyrebase
import os
import requests

class Users:
    user_dict = {}
    def __init__(self, user_id):
        self.user_dict['user_id'] = user_id

    def add_name(self, name):
        self.user_dict['name'] = user_id
    
    def add_latlng(self, latlng):
        self.user_dict['latlng'] = latlng
    
    def add_file_info(self, file_info):
        self.user_dict['file_info'] = file_info

    def add_contact(self, phone_no):
        self.user_dict['contact'] = phone_no

    def add_description(self, desc):
        self.user_dict['desc'] = desc
        
    def get_user_id(self):
        return self.user_dict['user_id']


content = {}

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def get_info(update):
    
    upd = copy.deepcopy(update.to_dict())
    # print(update)
    user_id = update.message.from_user.id
    content['user_id'] = str(user_id)
    # print(user_id)
    first_name = update.message.from_user.first_name
    last_name = update.message.from_user.last_name
    if last_name is None:
        content['name'] = first_name
    else:
        content['name'] = first_name + " " + last_name

    msg = update.message.text
    # print(msg)
    if upd.get('message').get('location') is not None:
        lat = upd.get('message').get('location').get('latitude')
        lng = upd.get('message').get('location').get('longitude')
        # print(str(lat) + ',' + str(lng))
        content['lat'] = str(lat)
        content['long'] = str(lng)

    if update.message.photo != []:
        # print(update.message.photo[-1].get_file()['file_path'])
        content['file_info'] = update.message.photo[-1].get_file()['file_path']



def echo(bot, update):
    if update.message.photo != []:
        get_info(update)
        location_keyboard = telegram.KeyboardButton(text="send_location", request_location=True)
        contact_keyboard = telegram.KeyboardButton(text="send_contact", request_contact=True)
        custom_keyboard = [[location_keyboard, contact_keyboard]]
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=update.message.chat_id,
                         text="Would you mind sharing your location and contact with me?",
                         reply_markup=reply_markup)


def location(bot, update):
    get_info(update)


def contact(bot, update):
    upd = update.to_dict()
    phone_no = str('+') + upd.get('message').get('contact').get('phone_number')
    content['contact'] = phone_no
    bot.send_message(chat_id=update.message.chat_id, text="Please let us know what the problem is...")
    # print(phone_no)

# def url_to_img(url):
#     response = requests.get(url)
#     img = Image.open(BytesIO(response.content))
#     img = np.asarray(img)
#     return img


def add_database(data):
    with open('api_key/config.json') as file:
        config = json.loads(file.read())
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
    storage = firebase.storage()

    db.child(data['user_id']).child('Name').set(data['name'])
    # db.child('user_id').child('Profile_pic').set(data['profile_pic'])
    image_path = db.child(data['user_id']).child('Complaints').push({'lat': data['lat'],
                                                                     'long': data['long'],
                                                                     'description': data['description']
                                                                     })
    img_data = requests.get(data['file_info']).content
    with open('image_name.jpg', 'wb') as handler:
        handler.write(img_data)
    storage.child('photos/' + str(data['user_id']) + image_path['name'] + '.jpg').put('image_name.jpg')
    os.remove('image_name.jpg')


def description(bot, update):
    desc = update.to_dict().get('message').get('text')
    content['description'] = desc
    bot.send_message(chat_id=update.message.chat_id, text="Thank you! Your complaint has been recorded! :)")

    print(content)

    add_database(content)


def main():
    TOKEN = open('./api_key/api.txt').read()

    updater = Updater(TOKEN)

    dp = updater.dispatcher

    # dp.add_handler(MessageHandler(Filters.text | Filters.photo | Filters.location, echo))
    dp.add_handler(MessageHandler(Filters.photo, echo))
    dp.add_handler(MessageHandler(Filters.location, location))
    dp.add_handler(MessageHandler(Filters.reply, contact))
    dp.add_handler(MessageHandler(Filters.text, description))

    # print(content)

    # log all errors
    dp.add_error_handler(error)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
    content = {}

