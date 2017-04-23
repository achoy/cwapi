#
# imagedata.py
#
from collections import namedtuple
import os
import math

ImageEntry = namedtuple('ImageEntry', 'pkey fname floc size w h title datetime')

def getAllFields():
    return 'pkey,fname,floc,size,w,h,title,datetime'

def fixnumber(numstr, trail, mult=1):
    numstr = numstr.replace(trail, '')
    fnum = float(numstr) * mult
    return math.floor(fnum)

def swizzle(name):
    return name.lower().replace('/','-')

def genkey(fname, floc):
    longkey = swizzle(fname)
    if len(floc) > 0:
        longkey = swizzle(floc) + '-' + longkey
    return os.path.splitext(longkey)[0]

def thumbfile(filename):
    return os.path.splitext(filename)[0] + '.png'

def decode_params(subprocess_in, seps = ' '):
    return subprocess_in.decode("utf-8").split(seps)

class Image(object):

    def __init__(self):
        self.inited = False

    def set_params(self, filepath='', width=0, height=0, size=0, datetime=''):
        if len(filepath) > 0:
            (floc, fname) = os.path.split(filepath)
            self.key1 = genkey(fname, floc)
            self.title = floc + ' ' + fname + ' ' + datetime
            self.data = ImageEntry(self.key1, fname, floc, size, width, height, self.title, datetime)
            self.inited = True

    def set_dict(self, idt):
        self.key1 = genkey(idt['fname'], idt['floc'])
        self.title = idt['floc'] + ' ' + idt['fname'] + ' ' + idt['datetime']
        self.data = ImageEntry(self.key1, idt['fname'], idt['floc'],
        idt['size'], idt['w'], idt['h'], self.title, idt['datetime'])
        self.inited = True

    def get_data(self):
        value = self.data
        return (value.pkey, value.fname, value.floc, value.size, value.w, value.h, value.title, value.datetime)

    def set_field(self, field, value):
        result = {
            'pkey':  lambda value : self.data._replace(pkey=value),
            'fname': lambda value : self.data._replace(fname=value),
            'floc':  lambda value : self.data._replace(floc=value),
            'title': lambda value : self.data._replace(title=value)
        }[field](value)
        return result

    def get_dict(self):
        value = self.data
        return { 'pkey' : value.pkey
        , 'fname' : value.fname
        , 'floc' : value.floc
        , 'size' : value.size
        , 'w' : value.w
        , 'h' : value.h
        , 'title' : value.title
        , 'datetime' : value.datetime }

    def get_url(self, urlRoot, fileType):
        return "{0}/{1}/{2}".format(urlRoot, fileType, self.get_key())

    def get_key(self):
        return self.data.pkey

    def name(self):
        return self.data.fname

    def loc(self):
        return self.data.floc

    def thumb(self):
        return thumbfile(self.name())

    def title(self):
        return self.data.title

    def printme(self):
        print('Image', self.data)
