from flask import Flask, render_template, request, redirect, jsonify
import json
import pyrebase
import datetime
from potholes.predict import predict_potholes
from pothole_classification.Classification import predict_severity
import cv2


app = Flask(__name__)

with open('api_key/config.json') as file:
    config = json.loads(file.read())

firebase = pyrebase.initialize_app(config)
db = firebase.database()
storage = firebase.storage()
auth = firebase.auth()


@app.route('/app')
def flutter_app():
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
    return jsonify(data_list)


# route to uploading images of id cards
@app.route('/image/upload', methods=['POST'])
def upload_image():
    
    if request.method == 'POST':

        # saving current timestamp
        current_time = str(datetime.datetime.now())
        
        # setting filename that is being received to current time stamp with its directory
        filename = 'temp/' + current_time + '.jpg'
        
        # get photo from android
        photo = request.files['photo']
        photo.save(filename)

        picture, no_boxes, pothole_coords = predict_potholes(filename)
        cv2.imwrite('detected.jpg', picture)
        content = {}
        if pothole_coords != []:
            predictions = predict_severity(current_time, pothole_coords)
            highest_severity = max(predictions)
            avg_severity = sum(predictions)/len(predictions)

            content['name'] = request.form['name']
            content['user_id'] = request.form['user_id']
            content['contact'] = request.form['contact']
            content['lat'] = request.form['lat']
            content['long'] = request.form['long']
            content['status'] = 'none'
            content['reason'] = 'none'
            content['highest_severity'] = str(highest_severity)
            content['avg_severity'] = str(avg_severity)
            
            add_database(content, filename)
            return jsonify({'found':True})
        else:
            return jsonify({'found':False})

        # return False if error
        return jsonify({'status':False})
    else:
        # if not POST, terminate
        return jsonify({'status':False})

def add_database(data, filename):
    with open('api_key/config.json') as file:
        config = json.loads(file.read())
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
    storage = firebase.storage()

    db.child('users/').child(data['user_id']).child('Name').set(data['name'])
    # db.child('user_id').child('Profile_pic').set(data['profile_pic'])
    image_path = db.child('users/').child(data['user_id']).child('Complaints').push({'lat': data['lat'],
                                                                     'long': data['long'],
                                                                     'status': 'none',
                                                                     'reason': 'none',
                                                                     'highest_severity': data['highest_severity'],
                                                                     'avg_severity': data['avg_severity']})
                                   
    storage.child('photos/' + str(data['user_id']) + image_path['name'] + '.jpg').put(filename)


if __name__ == '__main__':
    app.run(debug=False)
