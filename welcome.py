# Copyright 2015 IBM Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Modified by Lidia Dokuchaeva
#

import os
import json
import requests
import pygal
from pygal.style import DarkSolarizedStyle
from watson_developer_cloud import AlchemyLanguageV1
from flask import Flask, jsonify
from cloudant import cloudant
from cloudant.client import Cloudant
from cloudant.document import Document

app = Flask(__name__)

alchemy = AlchemyLanguageV1(api_key='6026adae6314a2a74df3c7a23a8e99d7f6e20c28')
vcap = json.loads(os.getenv("VCAP_SERVICES"))['cloudantNoSQLDB']

cl_username = vcap[0]['credentials']['username']
cl_password = vcap[0]['credentials']['password']
cl_url         = vcap[0]['credentials']['url']
cl_url  = "https://1a818337-f029-449a-8a03-d34f30877d1d-bluemix:b20bcbf26bac5fa4ed56df09b07755ac1d8ccf6e3d3ad1177902957c1ca192c0@1a818337-f029-449a-8a03-d34f30877d1d-bluemix.cloudant.com"

auth        = ( cl_username, cl_password )

@app.route('/')
def Welcome():
    return app.send_static_file('index.html')

@app.route('/myapp')
def WelcomeToMyapp():
    return 'Welcome again to my app running on Bluemix!'

@app.route('/api/people')
def GetPeople():
    list = [
        {'name': 'John', 'age': 28},
        {'name': 'Bill', 'val': 26}
    ]
    return jsonify(results=list)

@app.route('/api/people/<name>')
def SayHello(name):
    message = {
        'message': 'Hello ' + name
    }
    return jsonify(results=message)

# Testing Alchemy Connection
@app.route('/alchemytest')
def ConfirmConnection():
    key = os.environ.get('alchemyKey')
    return json.dumps(alchemy.targeted_sentiment(text='I love cats! Dogs are smelly.', targets=['cats', 'dogs'],
                                                 language='english'), indent=2)
@app.route('/alchemy')
def AnalyzeDoc():
    txt='http://www.news.uwa.edu.au/201610289155/international/fossilised-dinosaur-brain-tissue-identified-first-time'
    combined_operations = ['page-image', 'entity', 'keyword', 'title', 'author', 'taxonomy', 'concept', 'doc-emotion']
    return json.dumps(alchemy.combined(url=txt, extract=combined_operations), indent=2)

@app.route('/createdb/<db>')
def create_db(db):
    requests.put( cl_url + '/' + db, auth=auth )
    return 'Database %s created.' % db

@app.route('/testdb.svg')
def testDB():
    try:
        client = Cloudant(cl_username, cl_password, url=cl_url)
        #client = Cloudant('1a818337-f029-449a-8a03-d34f30877d1d-bluemix',
         #                'b20bcbf26bac5fa4ed56df09b07755ac1d8ccf6e3d3ad1177902957c1ca192c0',
        #url='https://1a818337-f029-449a-8a03-d34f30877d1d-bluemix
        # :b20bcbf26bac5fa4ed56df09b07755ac1d8ccf6e3d3ad1177902957c1ca192c0@1a818337-f029-449a-8a03-d34f30877d1d-bluemix.cloudant.com')
        client.connect()
        session = client.session()
    except Exception as ex:
        template = "An exception of type {0} occured. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        return "1: " + message
    try:
        my_database = client['x']
        if not my_database.exists():
            return 'Database does not exist'

    except Exception as ex:
        template = "An exception of type {0} occured. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        return "2: " + message
    # my_database = client['x']
    #list = ['0']
    #for document in my_database:
    #    list.append(document)
    #return jsonify(results=list)
    try:
        end_point = '{0}/{1}'.format(cl_url, 'x/_design/des/_view/new-view')
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
        bar_chart = pygal.Bar(width=1200, height=600,
                              explicit_size=True, title=title, style=DarkSolarizedStyle)
        bar_chart.x_labels = ['%s' % str(i['key']) for i in t]
        bar_chart.add('Relevance', relevance)
    except Exception as ex:
        template = "An exception of type {0} occured. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        return "3: " + message
    return bar_chart.render_response()

@app.route('/testdb')
def getHTML():
    html = """
                <html>
                     <head>
                          <title>Chart</title>
                     </head>
                      <body>
                        <figure>
                         <embed type="{{ url_for('testdb.svg') }}" src="%s" />
                         </figure>
                     </body>
                </html>
                """
    return html
port = os.getenv('PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port))
