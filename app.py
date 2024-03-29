#!/usr/bin/python
import os
from flask import Flask, request, send_from_directory, Response, jsonify
import time
import subprocess

app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/<firmware_name>')
def uploaded_file(firmware_name):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               "firmware/{}".format(firmware_name))


@app.route('/')
def home():
    return send_from_directory(app.config['UPLOAD_FOLDER'], 'index.html')

@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        file_name = '{}_firm'.format(time.time())
        dir_name = app.config['UPLOAD_FOLDER'] + '/firmware'
        file.save("{}/{}".format(dir_name, file_name))
        return jsonify({
            'firmware_name': file_name
        })
    return Response(status=401)


@app.route('/test')
def test():
    return 'HelloWorld'

if __name__ == '__main__':
    app.config['UPLOAD_FOLDER'] = os.getcwd()
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    app.run()
