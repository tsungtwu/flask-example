import urllib2
import unittest
import json
import os

from flask import Flask
from app import create_app as create_flask_app
from flask_testing import TestCase, LiveServerTestCase
from nose.tools import assert_equal



class TestCve(TestCase):
    fileDir = os.path.dirname(__file__)

    def create_app(self):
        return create_flask_app('testing')

    ## /api/cves/
    def test_no_parameter_cves(self):
        response = self.client.get("/api/cves/")
        print response
        self.assert400(response)
        self.assertEquals(response.json, \
                {'errors':{'time_from':'Time range begin'},\
                    'message':'Input payload validation failed'})

    def test_json_response_cves(self):
        response = self.client.get("/api/cves/?from=0&time_from=1382140800000&"\
                                    "time_to=1482140800000&size=2")

        with open(self.fileDir+'/testData/cves_result.json') as data_file:
            result = json.load(data_file)
        print response
        self.assertEqual(response.json, result)





    
    ## /api/cves/stat
    def test_no_parameter_stat(self):
        response = self.client.get("/api/cves/stat")
        print response
        self.assert400(response)
        self.assertEquals(response.json, \
                {'errors':{'time_from':'Time range begin'},\
                    'message':'Input payload validation failed'})

    def test_json_response_stat(self):
        response = self.client.get("/api/cves/stat?time_from=1382140800000&time_to=1482140800000")
        with open(self.fileDir+'/testData/cves_stat_result.json') as data_file:
            result = json.load(data_file)
        print response
        self.assert200(response)
        self.assertEqual(response.json, result)


    def test_timeFrom_format(self):
        response = self.client.get("/api/cves/stat?time_to=1382240800000&time_from=aabb%3F123?")
        print response
        self.assert400(response)
        self.assertEquals(response.json, \
                {"message": "Input payload validation failed", \
                    "errors": {"time_from": "Time range begin"}})

    def test_timeTo_format(self):
        response = self.client.get("/api/cves/stat?time_from=1382240800000&time_to=aabb%3F123?")
        print response
        self.assert400(response)
        self.assertEquals(response.json, \
                {"message": "Input payload validation failed", \
                    "errors": {"time_to": "Time range end"}})


    ## /api/cves/{cveId}
    def test_json_response_cve(self):
        response = self.client.get("/api/cves/CVE-2016-1824")
        with open(self.fileDir+'/testData/cve_result.json') as data_file:
            result = json.load(data_file)
        print response
        self.assertEquals(response.json, result)

    def test_cveid_format(self):
        response = self.client.get("/api/cves/cve-2016-1824")
        print response
        self.assertEquals(response.json, \
                {'message': 'parameter validation fail', \
                'error': {'field': 'cveId'}})

    def test_cveid_format_1(self):
        response = self.client.get("/api/cves/CVE-2016-18")
        print response
        self.assertEquals(response.json, \
                {'message': 'parameter validation fail', \
                'error': {'field': 'cveId'}})

    def test_cveid_format_2(self):
        response = self.client.get("/api/cves/AAA-2016-18")
        print response
        self.assertEquals(response.json, \
                {'message': 'parameter validation fail', \
                'error': {'field': 'cveId'}})
