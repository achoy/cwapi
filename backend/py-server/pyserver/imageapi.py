#
# imageapi.py
#

import os
import subprocess

from pyserver.imagedata import *

class ImageAPI(object):

    def __init__(self, rootPath, imagePath, thumbPath):
        self.rootPath = rootPath
        self.imagePath = imagePath
        self.thumbPath = thumbPath
        self.rplen = len(os.path.join(rootPath, imagePath)) + 1

    def getscandir(self):
        return os.path.join(self.rootPath, self.imagePath)

    def getpath(self, filename):
        return os.path.join(self.rootPath, self.imagePath, filename)

    def getthumb(self, filename):
        """Thumbnail will be a filename_w/o_ext.png"""
        thumbname = self.thumbfile(filename)
        return os.path.join(self.rootPath, self.thumbPath, thumbname)

    def thumbfile(self, filename):
        return os.path.splitext(filename)[0] + '.png'

    def decode_params(self, subprocess_in, seps = ' '):
        return subprocess_in.decode("utf-8").split(seps)

    def identify(self, ipath):
        # ipath = self.getpath(filename)
        result = subprocess.check_output(['identify', '-format', '"%w %h %b"', ipath])
        iout = self.decode_params(result)
        width = int(iout[0][1:])
        height = int(iout[1])
        if "MB" in iout[2]:
            size = fixnumber(iout[2], 'MB"', 1024.0)
        else:
            size = fixnumber(iout[2], 'KB"')
        result = subprocess.check_output(['identify', '-format', '"%[exif:*]"', ipath])
        try:
            ilines = self.decode_params(result, os.linesep)
            exifs = {}
            for line in ilines:
                parts = line.split('=')
                if len(parts) == 2:
                    exifs[parts[0]] = parts[1]
            if "exif:DateTime" in exifs:
                datetime = exifs['exif:DateTime']
            else:
                datetime = '2017:01:01 01:00:00'
        except UnicodeDecodeError:
            datetime = '2017:01:01 02:00:00'
            pass
        filename = ipath[self.rplen:]
        fullname = os.path.join(self.imagePath, filename)
        #thumbname = os.path.join(self.thumbPath, self.thumbfile(filename))
        print('stat: ', fullname, width, height, size, datetime)
        return Image(fullname, '', width, height, size, datetime)

    def make_thumbnail(self, filename):
        inpath = self.getpath(filename)
        outpath = self.getthumb(filename)
        result = subprocess.check_output(['convert', '-resize', '256x256^',
            '-gravity', 'Center', '-background', 'black', '-flatten', '-crop', '256x256+0+0',
            '+repage', inpath, outpath])
