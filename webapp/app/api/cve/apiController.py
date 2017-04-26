# -*- coding: utf-8 -*-
from elasticsearch_dsl import Q, A, Search
from flask_restplus import reqparse, Resource, Api, fields, Namespace, abort
import json, re
import os

from app.util.regToolBox import RegToolBox
from app.util.exceptionHandler import ExcepitonHandler
from .model import ApiModel

fileDir = os.path.dirname(__file__)


api = Namespace('cves', description='CVE operation')
apiModel = ApiModel(api)
regBox =  RegToolBox()
excpHandler = ExcepitonHandler()

# Request Parsing
parser = reqparse.RequestParser()
parser.add_argument('time_from', type=int, required=True, help='Time range begin')
parser.add_argument('time_to', type=int, required=True, help='Time range end')

parserCvesStat = parser.copy()


parserCves = parser.copy()
parserCves.add_argument('from', type=int, required=True, help='Offset from the first result')
parserCves.add_argument('size', type=int, required=True, help='Amount of cve item to be returned')

parserCves.add_argument('cveId', required=False, help='Id of CVE item')
parserCves.add_argument('vultype', required=False, help='vulType of CVE item')
parserCves.add_argument('product', required=False, help='CVE affected product')
parserCves.add_argument('vender', required=False, help='CVE affected vendor')


@api.route('/')
class CVEList(Resource):
    """CVEList resource"""
    def __init__(self, Resource):
        self.api = api

    @api.doc(description='Get Cve list by time range. \n\n ' \
                        'Time in UNIX Timestamp(milliseconds) format \n\n' \
                        '[Test query] time_from=1382140800000, time_to=1482140800000 \n\n' \
                        'cveId format: CVE-0000-0000 \n\n'
                        'Sorting Cve List' )
    @api.expect(parserCves)
    @api.response(200, 'Success', apiModel.cvesModel)
    @api.response(400, 'Parameter Validation Error', apiModel.paraErrorModel)
    def get(self):
        """Return list of CVEs."""
        args = parserCves.parse_args()

        # Parameter Validation
        for key in args:
            if args[key] == None:
                continue
            if key == 'cveId':
                if not regBox.checkCveId(args[key]):
                    return excpHandler.handle_validation_exception(key)
            elif type(args[key]) is unicode:
                if not regBox.checkWord(args[key]):
                    return excpHandler.handle_validation_exception(key)

        # Query Building

        size = args['size']
        fromOffset = args['from']

         # Integer Validation
        if (size > 2147483647) or (fromOffset > 2147483647):
            return excpHandler.handle_validation_exception(key)
        elif fromOffset+size > 10000:
            return excpHandler.handle_genernal_exception(\
                "[Elasticsearch]from + size must be less than or equal to: [10000]", "from, size", 400)

                
        # Build response json
        with open(fileDir+'/data/cves_result.json') as data_file:
            result = json.load(data_file)
        return result

@api.route('/stat')
class CVEInfo(Resource):
    def __init__(self, Resource):
        self.api = api
    
    @api.doc(description='CVE stat include top, pieChart.  \n\n' \
                ' `time_from`, `time_to` in UNIX Timestamp(milliseconds) format \n\n')
    @api.expect(parserCvesStat)
    @api.response(200, 'Success', apiModel.cveStatModel)
    def get(self):
        """ Get Information of CVE,include top List, count"""
        args = parser.parse_args()
        

        # Build response json
        with open(fileDir+'/data/cves_stat_result.json') as data_file:
            result = json.load(data_file)

        return result

    

@api.route('/<string:cveId>')
@api.doc(params={'cveId': 'Id of CVE item'})
class CVE(Resource):
    """ CVE with cveId"""
    def __init__(self, Resource):
        self.api = api
    
    @api.doc(description='Get Cve  by cve id. \n\n ' \
                    '* `cveId` format: CVE-0000-0000 \n\n' \
                    '* [Test query] `cveId`=CVE-2016-1824 \n\n')
    @api.response(200, 'Success', apiModel.cveModel)
    @api.response(400, 'Parameter Validation Error', apiModel.paraErrorModel)
    def get(self, cveId):
        """ Get cve by id """

        # Parameter Validation
        if not regBox.checkCveId(cveId):
            return excpHandler.handle_validation_exception('cveId')


        # Build response json
        with open(fileDir+'/data/cve_result.json') as data_file:
            result = json.load(data_file)
        if len(result) == 0:
            return {}
        else:
            return result

