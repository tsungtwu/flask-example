# -*- coding: utf-8 -*-
import json, re
import os

from flask_restplus import reqparse, Resource, Api, fields, Namespace, abort
from flask import request, session, make_response, redirect, Response

from app.util.regToolBox import RegToolBox
from app.util.exceptionHandler import ExcepitonHandler
from app.oauth import googleOauthService


api = Namespace('oauth', description='Oauth operation')
#apiModel = ApiModel(api)
regBox =  RegToolBox()
excpHandler = ExcepitonHandler()

parser = reqparse.RequestParser()
parser.add_argument('code', type=str, required=True, help='code')



@api.route('/google/login')
class GoogleLogin(Resource):
    """google resource"""
    def __init__(self, Resource):
        self.api = api

    @api.doc(description='Redirect to  Google Sign-in page. \n\n ' \
                        '* [Test] cannot direct test on swagger, '\
                        ' please copy the request url to new tab')
    def get(self):
        """ Google Sign-in entry """
        return googleOauthService.login()


@api.route('/google/logout')
class GoogleLogout(Resource):

    def __init__(self, Resource):
        self.api = api

    @api.doc(description='User logout. \n\n ' \
                        '* clear user session')
    def post(self):
        """ logout and clean session & cookie """
        googleOauthService.logout()

        resp = Response(json.dumps({'success':True, 'msg':'logout'}), mimetype='application/json')
        resp.set_cookie('authorized', 'False')
        session.pop('authorized')
        return resp

@api.route('/google/oauthcallback')
class GoogleAuth(Resource):
    def __init__(self, Resource):
        self.api = api

    @api.doc(description='Verify google oauthcallback code,' \
                    ' and get userinfo by access_token. \n\n ')
    @api.expect(parser)
    def get(self):
        """handle google oauthcallback"""

        auth_resp = googleOauthService.authorized(request)
        resp = Response(json.dumps(auth_resp), mimetype='application/json')

        if googleOauthService.get_access_token() != None:
            resp.set_cookie('authorized', 'True')
            session['authorized'] = True
        else:
            resp.set_cookie('authorized', 'False')
            session['authorized'] = False


        return resp


@api.route('/google/userinfo')
class GoogleUserinfo(Resource):
    def __init__(self, Resource):
        self.api = api

    @api.doc(description='Get `userinfo` by access_token.')
    def get(self):
        """ get user information by token"""

        userinfo = googleOauthService.get_userinfo()

        if userinfo != None:
            return userinfo
        else:
            return excpHandler.handle_genernal_exception('get userinfo Fail', 'access_token', 401)


