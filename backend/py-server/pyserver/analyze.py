#!flask/bin/python

import http.client
from urllib import request, parse, error
from flask import url_for
import base64
import traceback
import sys
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
        self.apiserver = 'westcentralus.api.cognitive.microsoft.com'

    def analyzeImage(self, urlRoot, image, categories):
        params = parse.urlencode({
            # requested parameters
            'visualFeatures' : categories,
            'language' : 'en'
        })

        try:
            conn = http.client.HTTPSConnection(self.apiserver)
            fileType = 'photos/full'
            body = { 'url' : image.get_url(urlRoot, fileType) }
            bodyenc = parse.urlencode(body)
            requestFrag = "/vision/v1.0/analyze?"
            print('type of params', type(params), 'type of requestFrag', type(requestFrag), 'type of body', type(bodyenc))
            print('apikey', self.apikey)
            requestUrl = '{}{}'.format(requestFrag, params)
            conn.request("POST", requestUrl, body=bodyenc, headers=self.headers)
            response = conn.getresponse()
            data = response.read()
            conn.close()
            return data
        except Exception as e:
            print("[Error {0}]".format(e))
            print(traceback.format_exception(None, e, e.__traceback__), file=sys.stderr, flush=True)
            return "Error"
