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
# from watson_developer_cloud import AlchemyLanguageV1
from flask import Flask, jsonify

app = Flask(__name__)

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
@app.route('/alchemy')
def ConfirmConnection():
    key = os.environ.get('alchemyKey')
    try:
        alchemy = AlchemyLanguageV1(api_key=key)
    except:
        return "Does not work..."
    return "Alchemy is connected!"

@app.route('/createdb/<db>')
def create_db(db):
    try:
        vcap = json.loads(os.getenv("VCAP_SERVICES"))['cloudantNoSQLDB']

        cl_username = vcap[0]['credentials']['username']
        cl_password = vcap[0]['credentials']['password']

        url         = vcap[0]['credentials']['url']
        auth        = ( cl_username, cl_password )

    except:
        return 'A Cloudant service is not bound to the application.  Please bind a Cloudant service and try again.'

    requests.put( url + '/' + db, auth=auth )
    return 'Database %s created.' % db

port = os.getenv('PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port))
