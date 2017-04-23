#!flask/bin/python

import http.client
from urllib import request, parse, error
from flask import url_for
import base64
from pyserver.imagedata import *

class ImageAnalysis(object):

    def __init__(self, app):
        self.app = app
        self.apikey = self.app.config['MSVAPIKEY']
        self.headers = {
            # request headers
            'Content-Type' : 'application/json',
            'Ocp-Apim-Subscription-Key' : self.apikey
        }
        self.apiserver = 'westus.api.cognitive.microsoft.com'

    def analyzeImage(self, urlRoot, image, categories):
        params = urllib.parse.urlencode({
            # requested parameters
            'visualFeatures' : categories,
            'language' : 'en'
        })

        try:
            conn = http.client.HTTPSConnection(self.apiserver)
            fileType = 'photos/full'
            body = { 'url' : image.get_url(urlRoot, fileType) }
            conn.request("POST", "/vision/v1.0/analyze?%s" % params, body, self.headers)
            response = conn.getresponse()
            data = response.read()
            conn.close()
        except Exception as e:
            print("[Error {0}] {1}".format(e.errno, e.strerror))

        return data
