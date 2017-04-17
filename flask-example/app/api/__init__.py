from flask_restplus import Api, Namespace

from app.api.cve.apiController import api as ns1
from app.api.tweet.apiController import api as ns2


api = Api(version='1', \
            title='Flask Restful plus Api', \
            doc='/api', \
            description='Document for Restful api', \
            contact='tsungwu@cyber00rn.org', \
            default='tweet')


api.add_namespace(ns1, path='/api/cves')
api.add_namespace(ns2, path='/api/tweet')
