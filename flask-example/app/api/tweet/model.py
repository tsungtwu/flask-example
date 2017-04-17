from flask_restplus import  fields

## Model definition
class ApiModel():
    def __init__(self, api):
        self.tweetModel = api.model('tweetModel', {
            "tweets.....": fields.String

        })


        self.tweetsModel = api.model('tweetsModel', {
            "totalTweetCount": fields.Integer,
            "retweetCount": fields.Integer,
            "retweets": fields.Nested(self.tweetModel),
            "tweets":fields.Nested(self.tweetModel),
            "tweetCount": fields.Integer,
        })


        self.fieldModel = api.model('fieldModel', {
            "field":fields.String
        })

        self.paraErrorModel = api.model('paraErrorModel', {
            "error":fields.Nested(self.fieldModel),
            "message":fields.String
        })

