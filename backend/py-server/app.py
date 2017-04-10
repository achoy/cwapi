#!flask/bin/python
from flask import Flask, jsonify

app = Flask(__name__)

photos = [
    { 'url': '1.jpeg', 'size': 36, 'title': 'Beachside AL' },
    { 'url': '2.jpeg', 'size': 19, 'title': 'Epica, 2' },
    { 'url': '3.jpeg', 'size': 41 },
    { 'url': '4.jpeg', 'size': 41, 'title': 'City museum AL'}
]

@app.route('/')
def index():
        return "CWAPI API Server"

@app.route('/photos/list.json')
def get_photos():
    return jsonify(photos)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
