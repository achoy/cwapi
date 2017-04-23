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

    def getscandir(self, part=''):
        if not part:
            return os.path.join(self.rootPath, self.imagePath)
        else:
            return os.path.join(self.rootPath, self.imagePath, part)

    def getthumbdir(self, part=''):
        if not part:
            return os.path.join(self.rootPath, self.thumbPath)
        else:
            return os.path.join(self.rootPath, self.thumbPath, part)

    def getpath(self, filename):
        return os.path.join(self.getscandir(), filename)

    def getthumb(self, filename):
        thumbname = thumbfile(filename)
        return os.path.join(self.getthumbdir(), thumbname)

    def get_size(self, istr):
        if "MB" in istr:
            return fixnumber(istr, 'MB"', 1024.0)
        elif "KB" in istr:
            return fixnumber(istr, 'KB"')
        elif "B" in istr:
            return fixnumber(istr, 'B"') // 1024
        return 0

    def identify(self, ipath):
        # ipath = self.getpath(filename)
        result = subprocess.check_output(['identify', '-format', '"%w %h %b"', ipath])
        iout   = decode_params(result)
        width  = int(iout[0][1:])
        height = int(iout[1])
        #if "MB" in iout[2]:
        #    size = fixnumber(iout[2], 'MB"', 1024.0)
        #else:
        #    size = fixnumber(iout[2], 'KB"')
        size = self.get_size(iout[2])
        result = subprocess.check_output(['identify', '-format', '"%[exif:*]"', ipath])
        try:
            ilines = decode_params(result, os.linesep)
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
        # truncate rootPath when passing in to Image()
        image = Image(filepath=ipath[self.rplen:], width=width, height=height, size=size, datetime=datetime)
        print(image.get_key())
        return image

    def make_thumbnail(self, image):
        fpath = os.path.join(image.loc(), image.name())
        self.make_thumbnail2(self.getpath(fpath), self.getthumb(fpath))

    def make_thumbnail2(self, inpath, outpath):
        #inpath = self.getpath(infile)
        #outpath = self.getthumb(outfile)
        (fpath, fname) = os.path.split(outpath)
        os.makedirs(fpath, exist_ok=True)
        result = subprocess.check_output(['convert', '-resize', '256x256^',
            '-gravity', 'Center', '-background', 'black', '-flatten', '-crop', '256x256+0+0',
            '+repage', inpath, outpath])
