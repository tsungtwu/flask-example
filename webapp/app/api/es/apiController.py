# -*- coding: utf-8 -*-
import json, re
import os

from flask_restplus import reqparse, Resource, Api, fields, Namespace, abort
from flask import request, session, make_response, redirect, Response
from elasticsearch_dsl import Q, A, Search

from app.util.regToolBox import RegToolBox
from app.util.exceptionHandler import ExcepitonHandler
from app.dao import daoPool


api = Namespace('es', description='Es operation')
esDAO = daoPool.esDAO

regBox =  RegToolBox()
excpHandler = ExcepitonHandler()


## Request parsing
parser = reqparse.RequestParser()
parser.add_argument('from', type=int, required=True, help='Offset from the first result')
parser.add_argument('size', type=int, required=True, help='Amount of cve item to be returned')

parserAgg = reqparse.RequestParser()
parserAgg.add_argument('size', type=int, required=True, help='Number of item to be returned')

@api.route('/search')
class GoogleLogin(Resource):
    """google resource"""
    def __init__(self, Resource):
        self.api = api
        esDAO.setIndexAndType("cve", "detail")

    
    @api.expect(parser)
    @api.doc(description='ESDAO Search example')    
    def get(self):
        """ Return es result """
        args = parser.parse_args()

        size = args['size']
        fromOffset = args['from']

        q = Q()
        sortQ = {}

        result = {}
        resultList = []
        resp = esDAO.search(q, sortQ, fromOffset, size)

        for hit in resp.to_dict()['hits']['hits']:
            resultList.append(hit)

        result['result'] = resultList

        return result

@api.route('/aggs')
class EsAggs(Resource):
    """ """
    def __init__(self, Resource):
        self.api = api
        esDAO.setIndexAndType("cve", "detail")


    @api.expect(parserAgg)
    @api.doc(description='ESDAO Aggregation example' \
                            'Get top `size` recent item')
    def get(self):
        """ get top  recent result """
        args = parserAgg.parse_args()

        topSize = args['size']

        q = Q()
        s = Search().query(q)
        sortDate = [{"original_release_date": {"order": "desc"}}]
        a_date = A('top_hits', sort=sortDate, size=topSize)
        s.aggs.metric('_topDate', a_date)

        result = {}
        resultList = []
        resp = esDAO.aggs(s).to_dict()
        for hit in resp['_topDate']['hits']['hits']:
            resultList.append(hit)

        result['_topDate'] = resultList

        return result
