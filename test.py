import wtforms
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
import json
import requests

class LinkForm(FlaskForm):
    name = StringField('URL', validators=[DataRequired()])

def alchemy_calls_left(api_key):
# This URL tells us how many calls we have left in a day
    URL = "http://access.alchemyapi.com/calls/info/GetAPIKeyInfo?apikey={}&outputMode=json".format(api_key)
# call AlchemyAPI, ask for JSON response
    response = requests.get(URL)
    calls_left = json.loads(response.content)
    return calls_left

cl_url  = "https://1a818337-f029-449a-8a03-d34f30877d1d-bluemix:b20bcbf26bac5fa4ed56df09b07755ac1d8ccf6e3d3ad1177902957c1ca192c0@1a818337-f029-449a-8a03-d34f30877d1d-bluemix.cloudant.com"
l = alchemy_calls_left(api_key='6026adae6314a2a74df3c7a23a8e99d7f6e20c28')
print(l)
