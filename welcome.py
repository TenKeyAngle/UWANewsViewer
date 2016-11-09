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
import csv
import pygal
import test
from test import LinkForm
from pygal.style import DarkSolarizedStyle
from watson_developer_cloud import AlchemyLanguageV1
from flask import Flask, jsonify, url_for, request, render_template, redirect
from cloudant import cloudant
from cloudant.client import Cloudant
from cloudant.document import Document

app = Flask(__name__)

alchemy = AlchemyLanguageV1(api_key='6026adae6314a2a74df3c7a23a8e99d7f6e20c28')
vcap = json.loads(os.getenv("VCAP_SERVICES"))['cloudantNoSQLDB']

cl_username = vcap[0]['credentials']['username']
cl_password = vcap[0]['credentials']['password']
cl_url         = vcap[0]['credentials']['url']
#cl_url  = "https://1a818337-f029-449a-8a03-d34f30877d1d-bluemix
# :b20bcbf26bac5fa4ed56df09b07755ac1d8ccf6e3d3ad1177902957c1ca192c0@1a818337-f029-449a-8a03-d34f30877d1d-bluemix.cloudant.com"

auth        = ( cl_username, cl_password )

s = DarkSolarizedStyle
s.font_family = 'Arial'
s.background = '#3b4b54'
s.plot_background = '#3b4b54'
s.tooltip_font_size *= 1.5
s.label_font_size *= 1.5
s.major_label_font_size *= 1.5
s.legend_font_size *= 1.5
s.title_font_size *= 1.5
s.value_font_size *= 1.5
s.tooltip_font_size *= 1.5

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

@app.route('/')
def Welcome():
    # form = LinkForm(request.args)
    form = LinkForm()
    #if request.method == 'GET':
       # if form.validate() == False:
       #     return render_template('index.html', form = form)
       # else:
       #     return redirect(url_for(GetUrl(), name=form.name.data))
    return render_template('index.html', form = form)
@app.route('/jsontest')
def JsonTest():
    j = {
        "selector": {
            "url":"http://www.news.uwa.edu.au/201611049179/aboriginal-people-inhabited-was-mid-west-coast-much-earlier-previously-thought"
        }
    }
    tofind = "{0}/{1}/_find/".format(cl_url, "test")
    a = requests.post(tofind, json=j)
    # return "<html><body>{0}</body></html>".format(a.text)
    return jsonify(a.text)

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

@app.route('/geturl', methods=('GET', 'POST'))
def GetUrl(name):
    url = name
    # end_point = '{0}/{1}'.format(cl_url, 'test/_design/des/_view/getlinks')
    # r = requests.get(end_point)
    # r = r.json()
    return render_template('layout.html', message=url)

@app.route('/scrape')
def Scrape():
    f = open('items/news.csv', 'rb')
    list = []
    try:
        reader = csv.reader(f)
        for row in reader:
            if row[0] != 'url' and row[0] != '':
                link = 'http://www.news.uwa.edu.au{0}'.format(row[0])
                list.append(link)
    except Exception as ex:
        template = "An exception of type {0} occured. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        return message
    combined_operations = ['title', 'authors', 'pub-date', 'entities', 'keywords',  'taxonomy', 'relations', 'concepts', 'doc-emotion']
    my_database = client['test']
    end_point = '{0}/{1}'.format(cl_url, 'test/_design/des/_view/getlinks')
    r = requests.get(end_point)
    r = r.json()
    t = []
    for item in r.get('rows'):
        t.append(item.get('value'))
    for i in list:
        if not i in t:
            data = alchemy.combined(url=i, extract=combined_operations)
            doc = my_database.create_document(data)
            if not doc.exists():
                return "Doc not created: " + jsonify(results=data)
    end_point = '{0}/{1}'.format(cl_url, 'test/_design/des/_view/getlinks')
    r = requests.get(end_point)
    r = r.json()
    t = []
    for item in r.get('rows'):
        t.append(item.get('value'))
    return jsonify(results=t)

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
        end_point = '{0}/{1}'.format(cl_url, 'test/_design/des/_view/new-view')
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
        bar_chart = pygal.Bar(title=title, style=s)
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
                     <title>Relevance Chart</title>
                     <meta charset="utf-8">
                     <meta http-equiv="X-UA-Compatible" content="IE=edge">
                     <meta name="viewport" content="width=device-width, initial-scale=1">
                     <link rel="stylesheet" href="static/stylesheets/style.css">
                   </head>
                      <body>
                        <figure>
                         <embed type="image/svg+xml" src="%s" />
                         </figure>
                     </body>
                </html>
                """ % url_for('testDB')
    return html
port = os.getenv('PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port))
