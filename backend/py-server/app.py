#!flask/bin/python
from flask import Flask, jsonify, make_response

app = Flask(__name__)

photos = [
    { 'url': 'Norwegian1.jpeg', 'size': 790, 'title': 'Norwegian 1' },
    { 'url': 'Norwegian2.jpeg', 'size': 785, 'title': 'Norwegian 2' },
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

@app.route('/photo/<path:filename>', methods=['GET'])
def download1(filename):
    dirpath = os.path.join(current_app.root_path, 'photos')
    return send_from_directory(directory=dirpath, filename=filename)

@app.route('/photolarge/<path:filename>', methods=['GET'])
def download2(filename):
    dirpath = os.path.join(current_app.root_path, 'photos')
    return send_from_directory(directory=dirpath, filename=filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
