import sys
import datetime
import logging
from elasticsearch import Elasticsearch
from flask_restplus import reqparse, Resource
from elasticsearch_dsl import Search, Q, A


reload(sys)
sys.setdefaultencoding('utf-8')
logger = logging.getLogger('ESDAO')
class ElasticsearchDAO():
    client = None
    indexES = None
    typeES = None
    esearch = None
    def __init__(self, host, port):
        url = "%s:%s" % (host, port)
        try:
            self.client = Elasticsearch([url], send_get_body_as="POST")
        except:
            logger.error('elasticsearch cannot connect')

    def setIndexAndType(self, index, type):
        self.indexES = index
        self.typeES = type
        self.esearch = Search(using=self.client, index=self.indexES, doc_type=self.typeES)


    def saveJson(self, json):
        """put json to ES """
        res = self.client.index(index=self.indexES, doc_type=self.typeES, body=json)
        return res


    def aggs(self, searchQuery):
        s = self.esearch.query()
        s.aggs = searchQuery.aggs
        s.query = searchQuery.query
        s = s[0:0]
        response = s.execute()

        return response.aggregations

    def search(self, q, sortQ, fromOffset, size):
        s = self.esearch.query(q) \
            .sort({"_score":{"order":"desc"}}, sortQ)
        s = s[fromOffset:fromOffset+size]
        response = s.execute()

        return response


