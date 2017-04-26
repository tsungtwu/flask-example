
import json
from flask import Flask, redirect, url_for, session, flash
from flask_oauth import OAuth
from urllib2 import URLError

from app.model.userModel import User
from app.dao import daoPool

oauth = OAuth()
sqlDAO = daoPool.sqlDAO


class GoogleOauthService():
    """ OAuth Service for google """

    REDIRECT_URI = 'http://localhost:5000/api/oauth/google/oauthcallback'
    app = None
    g_client = oauth.remote_app('google', \
                            base_url='https://www.google.com/accounts/', \
                          authorize_url='https://accounts.google.com/o/oauth2/auth', \
                          request_token_url=None, \
                          request_token_params={'scope':'https://www.googleapis.com/auth/userinfo.email', \
                                                'response_type':'code', 'access_type':'offline'}, \
                          access_token_url='https://accounts.google.com/o/oauth2/token', \
                          access_token_method='POST', \
                          access_token_params={'grant_type': 'authorization_code'}, \
                          consumer_key='', \
                          consumer_secret='')

    access_token = None

    def __init__(self, app):
        """ init g_client wiht client_id and client_secret """

        self.app = app
        self.g_client.consumer_key = app.config['GOOGLE_CLIENT_ID']
        self.g_client.consumer_secret = app.config['GOOGLE_CLIENT_SECRET']

    def login(self):
        """redirect to google Sign-in page """

        return self.g_client.authorize(callback=self.REDIRECT_URI)

    def logout(self):
        self.access_token = None

    def authorized(self, request):
        """ authodrize google oauthcallback code """

        ## verify code
        resp = self.g_client.handle_oauth2_response()

        self.access_token = resp['access_token']
        session['access_token'] = resp['access_token'], ''

        userinfo = self.get_userinfo()

        ##if First login, store userinfo to database
        user = User.query.filter_by(email=userinfo['email']).first()
        if user == None:

            newUser = User(userinfo['email'], userinfo['email'], resp['access_token'], \
                             resp['refresh_token'] if 'refresh_token' in resp != None else None)
            sqlDAO.session.add(newUser)
            sqlDAO.session.commit()

        return userinfo



    @g_client.tokengetter
    def tokengetter():
        return session.get('access_token')

    def get_access_token(self):
        return self.g_client.get_request_token()

    def get_userinfo(self):
        """ get access_token to get user information """

        if self.access_token == None:
            return None


        try:

            res = self.g_client.get('https://www.googleapis.com/oauth2/v1/userinfo')
            return res.data
        except URLError, e:
            if  e.code == 401:
                # Unauthorized - bad token
                return '401 Fail'
            return 'Fail'

        