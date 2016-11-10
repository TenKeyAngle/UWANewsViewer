import wtforms
from flask_wtf import FlaskForm
from wtforms import StringField, validators
from wtforms.validators import DataRequired
import json
import csv
import pygal
from pygal.style import BlueStyle
import requests
import operator

# Helper methods and classes for the main application

class LinkForm(FlaskForm):
    name = StringField('Search by News URL', validators=[validators.input_required()], default='Search by URL')

# Function to determine how many AlchemyAPI calls are left
# Gotten from https://gist.github.com/ianozsvald/4464247
def alchemy_calls_left(api_key):
    # This URL tells us how many calls we have left in a day
    URL = "http://access.alchemyapi.com/calls/info/GetAPIKeyInfo?apikey={}&outputMode=json".format(api_key)
    # call AlchemyAPI, ask for JSON response
    response = requests.get(URL)
    calls_left = response.json()
    return calls_left

def getHTML(json):

    return json

l = alchemy_calls_left(api_key='6026adae6314a2a74df3c7a23a8e99d7f6e20c28')
cl_url  = "https://1a818337-f029-449a-8a03-d34f30877d1d-bluemix:b20bcbf26bac5fa4ed56df09b07755ac1d8ccf6e3d3ad1177902957c1ca192c0@1a818337-f029-449a-8a03-d34f30877d1d-bluemix.cloudant.com"

j = {
    "selector": {
        "url": "http://www.news.uwa.edu.au/201611049179/aboriginal-people-inhabited-was-mid-west-coast-much-earlier-previously-thought"
    }
}
tofind = "{0}/{1}/_find/".format(cl_url, "uwanews")
a = requests.post(tofind, json=j)
a = a.json()
a = a['docs'][0]
print(a.get('_id'))