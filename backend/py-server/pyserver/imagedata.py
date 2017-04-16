#
# imagedata.py
#
from collections import namedtuple
import math

ImageEntry = namedtuple('ImageEntry', 'src msrc size w h title datetime')

def fixnumber(numstr, trail, mult=1):
    numstr = numstr.replace(trail, '')
    fnum = float(numstr) * mult
    return math.floor(fnum)

class Image(object):

    def __init__(self, filename, thumb, width, height, size, datetime):
        self.data = ImageEntry(filename, thumb, size, width, height, filename, datetime)

    #def __init__(self, idt):
    #    fname = idt['src']
    #    self.data = ImageEntry(fname, idt['msrc'], idt['size'], idt['w'], idt['h'], idt['title'], idt['datetime'])

    #def __init__(self):
    #    self.data = ImageEntry()

    def set_data(self, idt):
        fname = idt['src']
        self.data = ImageEntry(fname, idt['msrc'], idt['size'], idt['w'], idt['h'], idt['title'], idt['datetime'])

    def get_data(self):
        value = self.data
        return (value.src, value.msrc, value.size, value.w, value.h, value.title, value.datetime)

    def set_field(self, field, value):
        result = {
            'src':   lambda value : self.data._replace(src=value)
            'msrc':  lambda value : self.data._replace(msrc=value)
            'title': lambda value : self.data._replace(title=value)
        }[field](value)
        return result

    def get_dict(self):
        value = self.data
        return
        { 'src' : value.src
        , 'msrc' : value.msrc
        , 'size' : value.size
        , 'w' : value.w
        , 'h' : value.h
        , 'title' : value.title
        , 'datetime' : value.datetime }

    def name(self):
        return self.data.src
