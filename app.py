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
    # db.push('Hello')
    # storage.child('profile.jpg').put('profile.jpg')
    # print(get_config())
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
