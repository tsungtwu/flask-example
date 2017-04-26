

class ExcepitonHandler:
    def __init__(self):
        pass
    def handle_genernal_exception(self, msg, errorField, code):
        '''Return a custom message and 400 status code'''
        return {'message':msg, 'error':{'field':errorField}}, code

    def handle_validation_exception(self, errorField):
        '''Return a validation fail message and 400 status code'''
        return {'message':'parameter validation fail', 'error':{'field':errorField}}, 400
