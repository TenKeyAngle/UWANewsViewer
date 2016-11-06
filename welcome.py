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
url         = vcap[0]['credentials']['url']
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
    requests.put( url + '/' + db, auth=auth )
    return 'Database %s created.' % db

@app.route('/testdb')
def testDB():
    try:
        client = Cloudant(cl_username, cl_password, url=url)
    except:
        template = "An exception of type {0} occured. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        return message
    with Cloudant(cl_username, cl_password, account=url) as client:
        try:
            session = client.session()
        except:
            return "1"
        try:
            str = 'Username: {0}'.format(session['userCtx']['name'])
        except:
            return "2"
        # my_database = client['x']
        #list = ['0']
        #for document in my_database:
        #    list.append(document)
        #return jsonify(results=list)
        str = 'Username: {0}'.format(session['userCtx']['name'])
        return jsonify(results=str)

port = os.getenv('PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port))
