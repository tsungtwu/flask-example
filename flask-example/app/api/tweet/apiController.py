# -*- coding: utf-8 -*-
from elasticsearch_dsl import Q, A, Search
from elasticsearch_dsl.query import  Match
from flask_restplus import reqparse, Resource, Api, fields, Namespace

from .model import ApiModel
from app.util.exceptionHandler import ExcepitonHandler
from app.util.regToolBox import RegToolBox

import json
import os
fileDir = os.path.dirname(__file__)



api = Namespace('tweet', description='tweet operation')
apiModel = ApiModel(api)
regBox = RegToolBox()
excpHandler = ExcepitonHandler()



@api.route('/<string:cveId>')
@api.doc(params={'cveId': 'Id of CVE item'})
class Tweet(Resource):
    def __init__(self, Resource):
        self.api = api
        
    @api.doc(description='Get tweets  by cve id. \n\n ' \
                        '* [Test query] `cveId`=CVE-2016-1824')
    @api.response(200, 'Success', apiModel.tweetsModel)
    @api.response(400, 'Parameter Validation Error', apiModel.paraErrorModel)
    def get(self, cveId):
        """ Get List of tweet by cveId """
        # Parameter Validation
        if not regBox.checkCveId(cveId):
            return excpHandler.handle_validation_exception('cveId')

        with open(fileDir+'/data/tweets_result.json') as data_file:
            result = json.load(data_file)

        return result
       