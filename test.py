from watson_developer_cloud import AlchemyLanguageV1
from cloudant import cloudant
from cloudant.client import Cloudant
from cloudant.document import Document
from flask import jsonify
import json
import pygal
from pygal.style import DarkSolarizedStyle
import requests

cl_username = "1a818337-f029-449a-8a03-d34f30877d1d-bluemix"
cl_password = "b20bcbf26bac5fa4ed56df09b07755ac1d8ccf6e3d3ad1177902957c1ca192c0",
cl_url      = "https://1a818337-f029-449a-8a03-d34f30877d1d-bluemix:b20bcbf26bac5fa4ed56df09b07755ac1d8ccf6e3d3ad1177902957c1ca192c0@1a818337-f029-449a-8a03-d34f30877d1d-bluemix.cloudant.com"

auth = (cl_username, cl_password)
client = Cloudant(cl_username, cl_password, url=cl_url)



# Connect to the server
client.connect()

# Perform client tasks...
session = client.session()
my_database = client['x']

if my_database.exists():
    print('SUCCESS!')
end_point = '{0}/{1}'.format(cl_url, 'x/_design/des/_view/new-view')
#params = {'include_docs': 'true'}
r = requests.get(end_point)
print(r.json())
r = r.json()
t = []
for item in r.get('rows'):
    dict={}
    dict['key'] = item.get('key')
    dict['value'] = item.get('value')
    t.append(dict)
print(t)
doc = my_database['1d8c54f34b43c94894f01744608dbf46']
#print(json.dumps(doc))
# Disconnect from the server
relevance =  [float(i['value']) for i in t]
title = 'Most Relevant Topics'
bar_chart = pygal.Bar(width=1200, height=600,
                      explicit_size=True, title=title, style=DarkSolarizedStyle)
bar_chart.x_labels = ['%s' % str(i['key']) for i in t]
bar_chart.add('Relevance', relevance)
html = """
        <html>
             <head>
                  <title>%s</title>
             </head>
              <body>
                 %s
             </body>
        </html>
        """ % (title, bar_chart.render())
bar_chart.render_to_png('chart.png')
client.disconnect()

#doc = my_database['1d8c54f34b43c94894f01744608dbf46']
#end_point = 'https://1a818337-f029-449a-8a03-d34f30877d1d-bluemix
# :b20bcbf26bac5fa4ed56df09b07755ac1d8ccf6e3d3ad1177902957c1ca192c0@1a818337-f029-449a-8a03-d34f30877d1d-bluemix.cloudant.com/x/_design/des/_view/new-view'
# params = {"include_docs" : "true"}
#  response = client.r_session.get(end_point, params=params)
#return response.json()
# Define the end point and parameters
# Issue the request
#params = {'include_docs': 'true'}
# response = client.r_session.get(end_point, params=params)
# Display the response content
#return response.json()
#j = requests.get('https://1a818337-f029-449a-8a03-d34f30877d1d-bluemix
# :b20bcbf26bac5fa4ed56df09b07755ac1d8ccf6e3d3ad1177902957c1ca192c0@1a818337-f029-449a-8a03-d34f30877d1d-bluemix.cloudant.com/x/_design/des/_view/new-view')
#return j