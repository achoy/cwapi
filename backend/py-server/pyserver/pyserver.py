#!flask/bin/python
import os
import sqlite3
from flask import Flask, jsonify, make_response, current_app, \
    request, session, g, redirect, url_for, abort, \
    render_template, flash, send_from_directory

from pyserver.dirscan import *

app = Flask(__name__)
app.config.from_object(__name__)  # load config from this filename

# Load default config and override config
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'photos.db'),
    SECRET_KEY='supasecret',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('PHOTO_SETTINGS', silent=True)

dirtable = DirTable(app)

@app.cli.command('initdb')
def initdb_command():
    dirtable.init_db()
    print('Initialize the database.')

@app.teardown_appcontext
def close_db(error):
    dirtable.close_db(error)

@app.cli.command('update')
def update_command():
    dirscan = DirScan(large_files_path())
    dirtable.read_entries()
    dirtable.match_entries(dirscan)
    dirtable.show_entries()
    dirtable.store_entries()

def large_files_path():
    return os.path.join(current_app.root_path, 'photos/large')

def thumb_files_path():
    return os.path.join(current_app.root_path, 'photos/small')

#photos = [
#    { 'url': 'Norwegian1.jpeg', 'size': 790, 'title': 'Norwegian 1' },
#    { 'url': 'cool_balcony.jpg', 'size': 93, 'title': 'cool balcony' },
#    { 'url': 'doctor_who.jpg', 'size': 887, 'title': 'Doctor Who'}
#]

@app.route('/')
def index():
        return "CWAPI API Server"

@app.route('/photos/list.json')
def get_photos():
    dirtable.read_entries()
    resp = make_response(jsonify(dirtable.get_array_list()), 200)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/photos/thumb/<path:filename>', methods=['GET'])
def download1(filename):
    dirpath = thumb_files_path()
    return send_from_directory(directory=dirpath, filename=filename)

@app.route('/photo/full/<path:filename>', methods=['GET'])
def download2(filename):
    dirpath = large_files_path()
    return send_from_directory(directory=dirpath, filename=filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0:5000',debug=True)
