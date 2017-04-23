#!flask/bin/python
import os
import sqlite3
from flask_cache import Cache
from flask import Flask, jsonify, make_response, current_app, \
    request, session, g, redirect, url_for, abort, \
    render_template, flash, send_from_directory

from pyserver.dirscan import *
from pyserver.imageapi import ImageAPI

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
app.config.from_object(__name__)  # load config from this filename
app.config.from_envvar('FLASK_INFO')

# Load default config and override config
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'photos.db')
#    SECRET_KEY='supasecret',
#    USERNAME='admin',
#    PASSWORD='default'
))
#app.config.from_envvar('PHOTO_SETTINGS', silent=True)

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
    dirscan = DirScan(get_api())
    dirtable.read_entries()
    dirtable.match_entries(dirscan)
    #dirtable.show_entries()
    dirtable.store_entries()

def root_path():
    return current_app.root_path

def large_files_path():
    return os.path.join(root_path(), 'photos/large')

def thumb_files_path():
    return os.path.join(root_path(), 'photos/thumb')

def get_api():
    return ImageAPI(root_path(), 'photos/large', 'photos/thumb')

#photos = [
#    { 'url': 'Norwegian1.jpeg', 'size': 790, 'title': 'Norwegian 1' },
#    { 'url': 'cool_balcony.jpg', 'size': 93, 'title': 'cool balcony' },
#    { 'url': 'doctor_who.jpg', 'size': 887, 'title': 'Doctor Who'}
#]

@app.route('/')
def index():
        return "CWAPI API Server"

@app.route('/photos/list.json')
@cache.cached(timeout=60)
def get_photos():
    dirtable.read_entries()
    resp = make_response(jsonify(dirtable.get_array_list()), 200)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/photos/thumb/<string:pkey>', methods=['GET'])
def downloadT1(pkey):
    (dirpath, filename) = dirtable.get_thumb(pkey, get_api())
    if len(dirpath) == 0:
        return 'Cannot load thumbnail file from %s' % pkey
    print('loading from', dirpath, ':', filename)
    return send_from_directory(directory=dirpath, filename=filename)

@app.route('/photos/full/<string:pkey>', methods=['GET'])
def download2(pkey):
    (dirpath, filename) = dirtable.get_photo(pkey, get_api())
    if len(dirpath) == 0:
        return 'Cannot load file from %s' % pkey
    print('loading from', dirpath, ':', filename)
    return send_from_directory(directory=dirpath, filename=filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0:5000',debug=True)
