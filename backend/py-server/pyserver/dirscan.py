#
# dirscan.py
# Borrowed from exp_scan_lib.py
#

import os
import sched
import time
import sqlite3
import pprint
import subprocess
import math
from flask import g
from collections import namedtuple
from pyserver.imageapi import *

# DirEntry = namedtuple('DirEntry', 'src msrc size w h title')

class DirTable(dict):

    def __init__(self, app):
        self.app = app
        self.loaded = False

    # if not found, return this missing function
    def __missing__(self, key):
        return Image()

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
        if self.Loaded:
            return
        db = self.get_db()
        cur = db.execute('select * from metaphotos')
        entries = cur.fetchall()
        for e in entries:
            key = e['src']
            image = Image()
            image.set_data(e)
            self[key] = image

    def store_entries(self):
        db = self.get_db()
        db.execute('delete from metaphotos')
        rows = []
        for key, value in self.items():
            rows.append(value.get_data())
        db.executemany('insert into metaphotos (src, msrc, size, w, h, title, datetime) values(?,?,?,?,?,?,?)'
            , rows)
        db.commit()

    def updatefield(self, field, value, key):
        image = self[key]
        image.set_field(field, value)
        self[key] = image
        db = self.get_db()
        updatesql = 'update metaphotos set ' + field + ' = ? where key = ?'
        db.execute(updatesql, (value, key))
        db.commit()

    def show_entries(self):
        for key, value in self.items():
            print(value.get_data())

    def get_array_list(self):
        llist = []
        for key, value in self.items():
            llist.append( value.get_dict() )
        return llist

    def match_entries(self, dirscan):
        filelist = dirscan.scanwalk()
        for image in filelist:
            self[image.name()] = image


class DirScan(object):

    def __init__(self, rootPath, imagePath, thumbPath):
        self.imageAPI = ImageAPI(rootPath, imagePath, thumbPath)

    def isfilter(self, name):
        return name.lower().endswith(('.png', '.jpeg', '.jpg'))

    def scan(self):
        dirname = self.imageAPI.getscandir()
        filelist = os.listdir(dirname)
        if len(filelist) > 0:
            print("Scanning dir " + dirname + " count: " + str(len(filelist)))
        self.curFiles = [ self.imageAPI.identify(name) for name in filelist
            if self.isfilter(name) ]
        return self.curFiles

    def scanwalk(self):
        startpath = self.imageAPI.getscandir()
        self.curFiles = [self.imageAPI.identify(os.path.join(root, name))
                        for root, dirs, files in os.walk(startpath)
                        for name in files
                        if self.isfilter(name)]
        if len(self.curFiles) > 0:
            print("Walking ", startpath, " count: ", len(self.curFiles))
        return self.curFiles

    def getpath(self, name):
        return self.imageAPI.getpath(name)

    def getprops(self, name):
        filepath = self.getpath(name)
        statinfo = os.stat(filepath)
        return (name, statinfo.st_size // 1024)

    def getprops2(self, name):
        filepath = self.getpath(name)
        identifyout = subprocess.check_output(['identify', '-format', '"%w %h %b"', filepath])
        iout = identifyout.decode("utf-8").split(' ')
        width = int(iout[0][1:])
        height = int(iout[1])
        if "MB" in iout[2]:
            size = fixnumber(iout[2], 'MB"', 1024.0)
        else:
            size = fixnumber(iout[2], 'KB"')
        print('stat: ', filepath, width, height, size)
        return (name, width, height, size)
