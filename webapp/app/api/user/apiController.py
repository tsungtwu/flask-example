# -*- coding: utf-8 -*-
import json
import os
from elasticsearch_dsl import Q, A, Search
from elasticsearch_dsl.query import  Match
from flask_restplus import reqparse, Resource, Api, fields, Namespace

from .model import ApiModel
from app.util.exceptionHandler import ExcepitonHandler
from app.util.regToolBox import RegToolBox
from app.model.userModel import User as UserModel
from app.dao import daoPool

fileDir = os.path.dirname(__file__)



api = Namespace('users', description='user operation')
apiModel = ApiModel(api)
regBox = RegToolBox()
excpHandler = ExcepitonHandler()
sqlDAO = daoPool.sqlDAO

## Request Parsing
parser = reqparse.RequestParser()
parser.add_argument('username', required=True, help='name of user', location='args')
parser.add_argument('email',  required=False, help='email of user', location='args')


parserUpdate = reqparse.RequestParser()
parserUpdate.add_argument('username', required=False, help='name of user', location='args')
parserUpdate.add_argument('email',  required=False, help='email of user', location='args')


@api.route('/')
class Users(Resource):
    def __init__(self, Resource):
        self.api = api
    @api.doc(description='Get List of users . \n\n ')
    @api.response(200, 'Success', apiModel.usersModel)
    def get(self):
        """ Get all users """
        result = {}
        users = []

        resp = UserModel.query.all()
        if resp == None:
            return []

        for x in resp:
            users.append(x.to_dict())
        result['users'] = users
        return result

    @api.expect(parser, validate=False)
    @api.response(200, 'Success', apiModel.postModel)
    @api.doc(description='Add new user by username and email . \n\n ')
    def post(self):
        """ add user """
        args = parser.parse_args()
        user = UserModel(args['username'], args['email'] if args['email'] != None else None)
        sqlDAO.session.add(user)
        sqlDAO.session.commit()
        return {'success':True}




@api.route('/<string:id>')
@api.doc(params={'id': 'Id of user item'})
class User(Resource):
    def __init__(self, Resource):
        self.api = api
    @api.doc(description='Get User  by user id. \n\n ' \
                        '* [Test query] `id`=1')
    @api.response(200, 'Success', apiModel.userModel)
    def get(self, id):
        """ Get user by id """
        result = {}

        result = UserModel.query.get(id)

        return result.to_dict() if result != None else {'success':False, 'msg':'user does not exist'}

    @api.response(200, 'Success', apiModel.postModel)
    @api.doc(description='Delete User  by user id. \n\n ' \
                            '* [Test query] `id`=1')
    def delete(self, id):
        """ Delete user by id """
        
        user = UserModel.query.get(id)
        if user != None:
            sqlDAO.session.delete(user)
            sqlDAO.session.commit()
            return {'success': True}
        else:
            return {'success':False, 'msg':'user does not exist'}

    @api.expect(parserUpdate, validate=False)
    @api.response(200, 'Success', apiModel.postModel)
    def put(self, id):
        """ Update user by id """
        user = UserModel.query.get(id)
        if user != None:
            args = parserUpdate.parse_args()
            if args['username'] != None:
                user.username = args['username']
            if args['email'] != None:
                user.email = args['email']

            sqlDAO.session.commit()
            return {'success':True}
        else:
            return {'success':False, 'msg':'user does not exist'}