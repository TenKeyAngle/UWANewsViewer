import wtforms
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
import json
import csv
import pygal
from pygal.style import BlueStyle
import requests
import operator

class LinkForm(FlaskForm):
    name = StringField('URL', validators=[DataRequired()])

def alchemy_calls_left(api_key):
# This URL tells us how many calls we have left in a day
    URL = "http://access.alchemyapi.com/calls/info/GetAPIKeyInfo?apikey={}&outputMode=json".format(api_key)
# call AlchemyAPI, ask for JSON response
    response = requests.get(URL)
    calls_left = response.json()
    return calls_left

# print(relevance)
# print(t)
# print(list)

# end_point = '{0}/{1}'.format(cl_url, 'test/_design/des/_view/getrelevance')
# r = requests.get(end_point)
# r = r.json()
# #print(r)
# t = []
# rownum = 0
# for item in r.get('rows'):
#     dict={}
#     dict['key'] = item.get('key')
#     dict['value'] = item.get('value')
#     t.append(dict)
#     if rownum == 6:
#         break
#     else:
#         rownum += 1
# relevance =  [float(i['value']) for i in t]
# print(relevance)
