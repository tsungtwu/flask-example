from flask_oauth import OAuth
from .google.googleOauth import GoogleOauthService

oauth = OAuth()
googleOauthService = None

def init_oauth(app):
    global googleOauthService
    googleOauthService = GoogleOauthService(app)
