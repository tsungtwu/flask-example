import urllib2
import unittest


from flask import Flask
#from app.dao.esDAO import ElasticsearchReader
from app import create_app as create_flask_app
from flask_testing import TestCase, LiveServerTestCase
from nose.tools import assert_equal




class TestTwitter(TestCase):
    def create_app(self):
        return create_flask_app('testing')

    def test_json_response(self):
        response = self.client.get("/api/tweet/CVE-2016-1824")
        print response
        self.assertIsNotNone(response.json)

    def test_cveid_format_1(self):
        response = self.client.get("/api/tweet/cve-2016-1824")
        print response
        self.assertEquals(response.json, \
                {'message': 'parameter validation fail', \
                'error': {'field': 'cveId'}})

    def test_cveid_format_2(self):
        response = self.client.get("/api/tweet/CVE-2016-18")
        print response
        self.assertEquals(response.json, \
                {'message': 'parameter validation fail', \
                'error': {'field': 'cveId'}})

    def test_cveid_format_3(self):
        response = self.client.get("/api/tweet/AAA-2016-18")
        print response
        self.assertEquals(response.json, \
                {'message': 'parameter validation fail', \
                'error': {'field': 'cveId'}})

    def test_no_parameter(self):
        response = self.client.get("/api/tweet/")
        print response
        self.assert404(response)
