from flask_restplus import  fields

## Model definition
class ApiModel():
    def __init__(self, api):
        self.userModel = api.model('userModel', {
            "id": fields.Integer,
            "username": fields.String,
            "email": fields.String

        })


        self.usersModel = api.model('usersModel', {
            "users": fields.List(fields.Nested(self.userModel))
        })

        self.postModel = api.model('postModel', {
            "success":fields.Boolean
        })


        self.fieldModel = api.model('fieldModel', {
            "field":fields.String
        })

        self.paraErrorModel = api.model('paraErrorModel', {
            "error":fields.Nested(self.fieldModel),
            "message":fields.String
        })

