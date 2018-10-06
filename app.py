from flask import Flask, render_template
import json
import pyrebase

app = Flask(__name__)

with open('api_key/config.json') as file:
    config = json.loads(file.read())

firebase = pyrebase.initialize_app(config)
db = firebase.database()
storage = firebase.storage()


@app.route('/')
def index():
    data = db.get()
    data_dict = {}
    data_list = []
    for key, value in data.val().items():
        data_dict['Name'] = value['Name']
        for com_key, com_value in value['Complaints'].items():
            data_dict['lat'] = com_value['lat']
            data_dict['long'] = com_value['long']
            data_dict['description'] = com_value['description']
            # print(com_value['description'])
            path = 'photos/' + key + com_key + '.jpg'
            data_dict['image_url'] = storage.child(path).get_url(config).split("&token=")[0]
            # print(data_dict)
            data_list.append(data_dict.copy())
    print(data_list)
        # for
        # print(key)
        # print(value)
    return render_template('index.html', data = data_list)


@app.route('/user')
def user():
    data = db.get()
    data_dict = {}
    data_list = []
    for key, value in data.val().items():
        data_dict['Name'] = value['Name']
        for com_key, com_value in value['Complaints'].items():
            data_dict['lat'] = com_value['lat']
            data_dict['long'] = com_value['long']
            data_dict['description'] = com_value['description']
            path = 'photos/' + key + com_key + '.jpg'
            data_dict['image_url'] = storage.child(path).get_url(config).split("&token=")[0]
            data_list.append(data_dict.copy())
    return render_template('user.html', data = data_list)


@app.route('/panel')
def panel():
    data = db.get()
    data_dict = {}
    data_list = []
    for key, value in data.val().items():
        data_dict['Name'] = value['Name']
        for com_key, com_value in value['Complaints'].items():
            data_dict['lat'] = com_value['lat']
            data_dict['long'] = com_value['long']
            data_dict['description'] = com_value['description']
            path = 'photos/' + key + com_key + '.jpg'
            data_dict['image_url'] = storage.child(path).get_url(config).split("&token=")[0]
            data_list.append(data_dict.copy())
    print(data_list)
    return render_template('panel.html', data = data_list)


@app.route('/locations')
def locations():
    data = db.get()
    data_dict = {}
    data_list = []
    for key, value in data.val().items():
        data_dict['Name'] = value['Name']
        for com_key, com_value in value['Complaints'].items():
            data_dict['lat'] = com_value['lat']
            data_dict['long'] = com_value['long']
            data_dict['description'] = com_value['description']
            path = 'photos/' + key + com_key + '.jpg'
            data_dict['image_url'] = storage.child(path).get_url(config).split("&token=")[0]
            data_list.append(data_dict.copy())
    print(data_list)
    return render_template('locations.html', data = data_list)


if __name__ == '__main__':
    app.run(debug=True)
