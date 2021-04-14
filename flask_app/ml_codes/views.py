from flask import render_template, request, Blueprint
import os

ml_codes = Blueprint('ml_codes', __name__)

@ml_codes.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        client_record = request.files['audio_data'].read()
        f = open(os.getcwd() + '/client/audio.wav', 'wb')
        # print(client_record)
        f.write(client_record)
        f.close()
        print('FILE IS UPLOADED!!')
        return render_template('home.html', request='POST')
    return render_template('home.html')

@ml_codes.route('/result', methods=['POST', 'GET'])
def result():
    # ml code goes here
    return render_template('result.html')