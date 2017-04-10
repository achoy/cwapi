#!flask/bin/python
import os
from flask import Flask, jsonify, make_response, current_app, send_from_directory

app = Flask(__name__)

photos = [
    { 'url': 'Norwegian1.jpeg', 'size': 790, 'title': 'Norwegian 1' },
    { 'url': 'cool_balcony.jpg', 'size': 93, 'title': 'cool balcony' },
    { 'url': 'doctor_who.jpg', 'size': 887, 'title': 'Doctor Who'}
]

@app.route('/')
def index():
        return "CWAPI API Server"

@app.route('/photos/list.json')
def get_photos():
    resp = make_response(jsonify(photos), 200)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/thumb/<path:filename>', methods=['GET'])
def download1(filename):
    dirpath = os.path.join(current_app.root_path, 'photos/small')
    return send_from_directory(directory=dirpath, filename=filename)

@app.route('/photo/<path:filename>', methods=['GET'])
def download2(filename):
    dirpath = os.path.join(current_app.root_path, 'photos/large')
    return send_from_directory(directory=dirpath, filename=filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
