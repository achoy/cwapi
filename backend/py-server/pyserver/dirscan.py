#
# dirscan.py
# Borrowed from exp_scan_lib.py
#

import os
import sched
import time
import sqlite3
import pprint
from flask import g
from collections import namedtuple

DirEntry = namedtuple('DirEntry', 'url size description')

class DirTable(dict):

    def __init__(self, app):
        self.app = app

    # if not found, return this missing function
    def __missing__(self, key):
        return DirEntry('', 0, '')

    def connect_db(self):
        """Connect to specific database"""
        rv = sqlite3.connect(self.app.config['DATABASE'])
        rv.row_factory = sqlite3.Row
        return rv

    def get_db(self):
        """Open database connection"""
        if not hasattr(g, 'sqlite_db'):
            g.sqlite_db = self.connect_db()
        return g.sqlite_db

    def init_db(self):
        db = self.get_db()
        with self.app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

    def close_db(self, error):
        if hasattr(g, 'sqlite_db'):
            g.sqlite_db.close()

    def read_entries(self):
        db = self.get_db()
        cur = db.execute('select id, url, size, title from metaphotos')
        entries = cur.fetchall()
        for e in entries:
            self[e['url']] = DirEntry(e['url'], e['size'], e['title'])

    def store_entries(self):
        db = self.get_db()
        db.execute('delete from metaphotos')
        rows = []
        for key, value in self.items():
            rows.append((value.url, value.size, value.description))
        db.executemany('insert into metaphotos (url, size, title) values(?,?,?)', rows)
        db.commit()

    def show_entries(self):
        for key, value in self.items():
            print(value)

    def get_array_list(self):
        llist = []
        for key, value in self.items():
            llist.append({'url': value.url, 'size': value.size, 'title': value.description})
        return llist

    def match_entries(self, dirscan):
        filelist = dirscan.scan()
        for name, size in filelist:
            if name in self:
                found = self[name]
                found.url = name
                found.size = size
                found.description = name
                self[name] = found
            else:
                self[name] = DirEntry(name, size, name)

class DirScan(object):

    def __init__(self, scanFolder1):
        self.scanFolder1 = scanFolder1

    def isfilter(self, name):
        return not name.startswith('.')

    def scan(self):
        dirname = self.scanFolder1
        filelist = os.listdir(dirname)
        if len(filelist) > 0:
            print("Scanning dir " + dirname + " count: " + str(len(filelist)))
        self.curFiles = [ self.getprops(name) for name in filelist if self.isfilter(name) ]
        return self.curFiles

    def getpath(self, name):
        return os.path.join(self.scanFolder1, name)

    def getprops(self, name):
        filepath = self.getpath(name)
        statinfo = os.stat(filepath)
        return (name, statinfo.st_size // 1024)
