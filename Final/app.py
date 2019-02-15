from flask import Flask, render_template, request, redirect, jsonify
import json
import pyrebase

app = Flask(__name__)

with open('api_key/config.json') as file:
    config = json.loads(file.read())

firebase = pyrebase.initialize_app(config)
db = firebase.database()
storage = firebase.storage()
auth = firebase.auth()


@app.route('/admin-panel')
def index():
    data = db.child('users/').get()
    data_dict = {}
    data_list = []
    for key, value in data.val().items():
        data_dict['Name'] = value['Name']
        data_dict['user_id'] = key
        for com_key, com_value in value['Complaints'].items():
            data_dict['lat'] = com_value['lat']
            data_dict['long'] = com_value['long']
            # data_dict['description'] = com_value['description']
            data_dict['complaint_id'] = com_key
            data_dict['status'] = com_value['status']
            data_dict['reason'] = com_value['reason']
            data_dict['highest_severity'] = com_value['highest_severity']
            data_dict['avg_severity'] = com_value['avg_severity']
            # print(com_value['description'])
            path = 'photos/' + key + com_key + '.jpg'
            data_dict['image_url'] = storage.child(path).get_url(config).split("&token=")[0]
            # print(data_dict)
            data_list.append(data_dict.copy())
    print(data_list)
    return render_template('index.html', data = data_list)


@app.route('/')
def user():
    data = db.child('users/').get()
    data_dict = {}
    data_list = []
    for key, value in data.val().items():
        data_dict['Name'] = value['Name']
        for com_key, com_value in value['Complaints'].items():
            data_dict['lat'] = com_value['lat']
            data_dict['long'] = com_value['long']
            # data_dict['description'] = com_value['description']
            data_dict['status'] = com_value['status']
            data_dict['reason'] = com_value['reason']
            path = 'photos/' + key + com_key + '.jpg'
            data_dict['image_url'] = storage.child(path).get_url(config).split("&token=")[0]
            data_list.append(data_dict.copy())
    return render_template('user.html', data = data_list)

# @app.route('/panel')
# def panel():
#     data = db.get()
#     data_dict = {}
#     data_list = []
#     for key, value in data.val().items():
#         data_dict['Name'] = value['Name']
#         for com_key, com_value in value['Complaints'].items():
#             data_dict['lat'] = com_value['lat']
#             data_dict['long'] = com_value['long']
#             data_dict['description'] = com_value['description']
#             path = 'photos/' + key + com_key + '.jpg'
#             data_dict['image_url'] = storage.child(path).get_url(config).split("&token=")[0]
#             data_list.append(data_dict.copy())
#     print(data_list)
#     return render_template('panel.html', data = data_list)


@app.route('/locations')
def locations():
    data = db.child('users/').get()
    data_dict = {}
    data_list = []
    for key, value in data.val().items():
        data_dict['Name'] = value['Name']
        for com_key, com_value in value['Complaints'].items():
            data_dict['lat'] = com_value['lat']
            data_dict['long'] = com_value['long']
            # data_dict['description'] = com_value['description']
            path = 'photos/' + key + com_key + '.jpg'
            data_dict['image_url'] = storage.child(path).get_url(config).split("&token=")[0]
            data_list.append(data_dict.copy())
    print(data_list)
    return render_template('locations.html', data = data_list)


@app.route('/del_complaint', methods=['POST'])
def del_complaint():
    reason = request.form.get('reason')
    user_id = request.form.get('user_id')
    complaint_id = request.form.get('complaint_id')
    db.child('users/').child(user_id).child("Complaints").child(complaint_id).child('status').set('false')
    db.child('users/').child(user_id).child("Complaints").child(complaint_id).child('reason').set(reason)
    return redirect('/')


@app.route('/approve', methods=['POST'])
def approve():
    user_id = request.form.get('user_id')
    complaint_id = request.form.get('complaint_id')
    db.child('users/').child(user_id).child("Complaints").child(complaint_id).child('status').set('true')
    return redirect('/')

# New admin signup
@app.route('/admin-signup', methods=['POST'])
def adminSignup():
    email = request.form.get('email')
    password =request.form.get('password')
    user = auth.create_user_with_email_and_password(email, password)
    db.child('admins/').push({'email': email})
    if(user is not None):
        redirect('/admin-panel')

# Admin login
@app.route('/admin-signin', methods=['POST'])
def adminSignin():
    email = request.form.get('email')
    password =request.form.get('password')
    user = auth.sign_in_with_email_and_password(email, password)
    if(user is not None):
        redirect('/admin-panel')

@app.route('/login')
def login():
        return render_template('login.html')        


@app.route('/signup')
def signup():
        return render_template('signup.html')


if __name__ == '__main__':
    app.run(debug=True)
