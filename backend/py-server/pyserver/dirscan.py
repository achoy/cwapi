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

DirEntry = namedtuple('DirEntry', 'src msrc size w h title')

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
        cur = db.execute('select * from metaphotos')
        entries = cur.fetchall()
        for e in entries:
            key = e['src']
            self[key] = DirEntry(key, e['msrc'], e['size'], e['w'], e['h'], e['title'])

    def store_entries(self):
        db = self.get_db()
        db.execute('delete from metaphotos')
        rows = []
        for key, value in self.items():
            rows.append((value.src, value.msrc, value.size, value.w, value.h, value.title))
        db.executemany('insert into metaphotos (src, msrc, size, w, h, title) values(?,?,?,?,?,?)'
            , rows)
        db.commit()

    def show_entries(self):
        for key, value in self.items():
            print(value)

    def get_array_list(self):
        llist = []
        for key, value in self.items():
            llist.append( { 'src' : value.src
            , 'msrc' : value.msrc
            , 'size' : value.size
            , 'w' : value.w
            , 'h' : value.h
            , 'title' : value.title } )
        return llist

    def match_entries(self, dirscan):
        filelist = dirscan.scan()
        for (name, width, height, size) in filelist:
            if name in self:
                found = self[name]
                found.src   = name
                found.msrc  = name
                found.w     = width
                found.h     = height
                found.size  = size
                found.title = name
                self[name] = found
            else:
                self[name] = DirEntry(name, name, size, width, height, name)

def fixnumber(numstr, trail, mult=1):
    numstr = numstr.replace(trail, '')
    fnum = float(numstr) * mult
    return math.floor(fnum)

class DirScan(object):

    def __init__(self, scanFolder1):
        self.scanFolder1 = scanFolder1

    def isfilter(self, name):
        return name.lower().endswith(('.png', '.jpeg', '.jpg'))

    def scan(self):
        dirname = self.scanFolder1
        filelist = os.listdir(dirname)
        if len(filelist) > 0:
            print("Scanning dir " + dirname + " count: " + str(len(filelist)))
        self.curFiles = [ self.getprops2(name) for name in filelist if self.isfilter(name) ]
        return self.curFiles

    def getpath(self, name):
        return os.path.join(self.scanFolder1, name)

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
