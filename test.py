import wtforms
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
import json
import pygal
from pygal.style import BlueStyle
import requests

class LinkForm(FlaskForm):
    name = StringField('URL', validators=[DataRequired()])

def alchemy_calls_left(api_key):
# This URL tells us how many calls we have left in a day
    URL = "http://access.alchemyapi.com/calls/info/GetAPIKeyInfo?apikey={}&outputMode=json".format(api_key)
# call AlchemyAPI, ask for JSON response
    response = requests.get(URL)
    calls_left = response.json()
    return calls_left

cl_url  = "https://1a818337-f029-449a-8a03-d34f30877d1d-bluemix:b20bcbf26bac5fa4ed56df09b07755ac1d8ccf6e3d3ad1177902957c1ca192c0@1a818337-f029-449a-8a03-d34f30877d1d-bluemix.cloudant.com"
l = alchemy_calls_left(api_key='6026adae6314a2a74df3c7a23a8e99d7f6e20c28')
print(l)

end_point = '{0}/{1}'.format(cl_url, 'test/_design/des/_view/getrelevance')
r = requests.get(end_point)
r = r.json()
#print(r)
t = []
for item in r.get('rows'):
    dict={}
    dict['key'] = item.get('key')
    dict['value'] = item.get('value')
    t.append(dict)
#print(t)


def testDB():
    try:
        end_point = '{0}/{1}'.format(cl_url, 'test/_design/des/_view/getrelevance')
        r = requests.get(end_point)
        r = r.json()
        t = []
        for item in r.get('rows'):
            dict={}
            dict['key'] = item.get('key')
            dict['value'] = item.get('value')
            t.append(dict)
        relevance =  [float(i['value']) for i in t]
        title = 'Most Relevant Topics'
    except Exception as ex:
        template = "An exception of type {0} occured. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        return "3: " + message
    try:
        bar_chart = pygal.Bar(title=title, style=BlueStyle)
        bar_chart.x_labels = ['%s' % str(i['key']) for i in t]
        bar_chart.add('Relevance', relevance)
    except Exception as ex:
        template = "An exception of type {0} occured. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        return "4: " + message
    bar_chart.render_to_file('sample.svg')
    return "success"

print(testDB())