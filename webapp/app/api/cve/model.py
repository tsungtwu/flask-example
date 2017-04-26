from flask_restplus import  fields

## Model definition
class ApiModel():
    def __init__(self, api):
        self.zeroPriceModel = api.model('zeroPriceModel', {
            "lower": fields.Integer,
            "range": fields.String,
            "upper":fields.Integer
        })

        self.cveModel = api.model('cveModel', {
            "CVE_ID": fields.String,
            "CVSS_V2_base_score": fields.Float,
            "NVD_CWEID": fields.String,
            "cvedetail_affected_product": fields.String,
            "cvedetail_affected_vender": fields.String,
            "cvedetail_vultype": fields.String,
            "exploit": fields.Integer,
            "exploit_date": fields.Integer,
            "original_release_date": fields.Integer,
            "overview": fields.String,
            "retweet_count": fields.Integer,
            "tweet_count": fields.Integer,
            "zeroday_price": fields.Nested(self.zeroPriceModel)
            })

        self.cvesModel = api.model('cvesModel', {
            "cveCount" : fields.Integer,
            "cves":fields.List(fields.Nested(self.cveModel))
        })


        self.bucketModel = api.model('bucketModel', {
            "data":fields.Integer,
            "label":fields.String
        })
        self.pieModel = api.model('pieModel',{
            "_priceAgg":fields.List(fields.Nested(self.bucketModel)),
            "_vulTypeAgg":fields.List(fields.Nested(self.bucketModel)),
            "_exploitAgg":fields.List(fields.Nested(self.bucketModel)),
            "_severityAgg":fields.List(fields.Nested(self.bucketModel))
        })

        self.topModel = api.model('topModel',{
            "_topDate":fields.List(fields.Nested(self.cveModel)),
            "_topSeverity":fields.List(fields.Nested(self.cveModel)),
            "_topPrice":fields.List(fields.Nested(self.cveModel)),
            "_topExploit":fields.List(fields.Nested(self.cveModel)),
            "_topPopular":fields.List(fields.Nested(self.cveModel))

            
        })
        self.cveStatModel = api.model('statModel', {
            "top":fields.List(fields.Nested(self.topModel), description='array of top stat'),
            "pieStat":fields.List(fields.Nested(self.pieModel), description='array of piechart Stat'),
            "cveCount": fields.Integer(description='cve Count'),
            "tweetCount": fields.Integer(description='total tweet Count(tweet + retweet)')

            })

        self.fieldModel = api.model('fieldModel', {
            
            "field":fields.String
        })

        self.paraErrorModel = api.model('paraErrorModel', {
            "error":fields.Nested(self.fieldModel),
            "message":fields.String
        })