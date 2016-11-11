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
# This project was modified by Lidia Dokuchaeva - 21331893
# 11/11/2016
#

import os
import json
import requests
import csv
import operator
import pygal
import helper
from helper import LinkForm, alchemy_calls_left, getDocDeets, JForm, getSearchResults
from pygal.style import DarkSolarizedStyle
from watson_developer_cloud import AlchemyLanguageV1
from flask import Flask, jsonify, url_for, request, render_template, redirect, Markup
from cloudant import cloudant
from cloudant.client import Cloudant
from cloudant.document import Document

app = Flask(__name__)

#Connect required services
api_key='6026adae6314a2a74df3c7a23a8e99d7f6e20c28'
alchemy = AlchemyLanguageV1(api_key=api_key)
vcap = json.loads(os.getenv("VCAP_SERVICES"))['cloudantNoSQLDB']

cl_username = vcap[0]['credentials']['username']
cl_password = vcap[0]['credentials']['password']
cl_url         = vcap[0]['credentials']['url']
cl_url  = "https://1a818337-f029-449a-8a03-d34f30877d1d-bluemix:b20bcbf26bac5fa4ed56df09b07755ac1d8ccf6e3d3ad1177902957c1ca192c0@1a818337-f029-449a-8a03-d34f30877d1d-bluemix.cloudant.com"

auth = ( cl_username, cl_password )

# Modifies Style for Graphs
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

#Connect to Cloudant and the dtabase in question
try:
    client = Cloudant(cl_username, cl_password, url=cl_url)
    client.connect()
    session = client.session()
    database = client['uwanews']
    if not database.exists():
    	print("Database uwanews not found.")
except Exception as ex:
    template = "An exception of type {0} occured. Arguments:\n{1!r}"
    message = template.format(type(ex).__name__, ex.args)

# Begin App

# Return main page, with URL search
@app.route('/')
def Welcome():
    form = LinkForm(request.args, csrf_enabled=False)
    if request.method == 'GET':
        if form.validate() == False:
            # If form is not valid, load the form
            return render_template('index.html', form=form)
        else:
            # If form is valid, get results
            return redirect(url_for('GetUrl'))
    return render_template('index.html', form=form)

# A test page that shows how the JSON fetch works
@app.route('/jsontest')
def JsonTest():
    # j = {
    #     "selector": {
    #         "url":"http://www.news.uwa.edu.au/201611049179/aboriginal-people-inhabited-was-mid-west-coast-much-earlier-previously-thought"
    #     }
    # }
    # tofind = "{0}/{1}/_find/".format(cl_url, "uwanews")
    # a = requests.post(tofind, json=j)
    command = "scrapy runspider linkscraper.py -o news1.csv -t csv"
    return_code = os.system(command)
    if return_code == 1:
        return "Success"
    else:
        return "Failure: check logs for more details."

# Search database by keyword
@app.route('/keyword/<word>')
def SearchDB(word):
    j = {
      "selector": {
         "$text": word
       },
        # Which fields to include in the results
       "fields": [
         "_id",
         "_rev",
         "url",
         "title",
      "publicationDate"
     ],
        # Sort chronologically
        "sort": [
     { 
        "publicationDate:string":"desc"
      }
     ]
    }
    # use RESTful API to get results
    tofind = "{0}/{1}/_find/".format(cl_url, "uwanews")
    a = requests.post(tofind, json=j)
    a = a.json()
    a = a['docs']
    if len(a) == 0:
        # If no documents match criteria, inform user
        return render_template('layout.html', message="No documents found.")
    else:
        # If documents match criteria, display them to user
        return render_template('layout.html', message=Markup(getSearchResults(json=a)))

# Get details for a specific news article
@app.route('/geturl')
def GetUrl():
    url = request.args.get("name")
    if not url[:4] == "http":
        redirect(url_for('SearchDB', word=url))
    j = {
        "selector": {
            "url": url
        }
    }
    # use RESTful API to get results
    tofind = "{0}/{1}/_find/".format(cl_url, "uwanews")
    a = requests.post(tofind, json=j)
    a = a.json()
    a = a['docs']
    try:
        # If documents found, display results
        doc = database[a[0].get('_id')]
        return render_template('layout.html', message=Markup(getDocDeets(json=doc)))
    except:
        # If no documents found, let user know
        return render_template('layout.html', message="No documents found.")

# The method that analyzes URLs from the CSV file - should be run automatically
@app.route('/scrape')
def Scrape():
    # Check that limit not surpassed
    al = alchemy_calls_left(api_key=api_key)
    if not al['consumedDailyTransactions'] < al['dailyTransactionLimit']:
        # If limit surpassed, return a string letting user know
        return jsonify(al)
    # If limint not surpassed, iterate through news.csv to get URLs
    f = open('items/news.csv', 'r')
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
    # Initialize parameters for analysis
    combined_operations = ['title', 'authors', 'pub-date', 'entities', 'keywords',  'taxonomy', 'relations', 'concepts', 'doc-emotion']
    end_point = '{0}/{1}'.format(cl_url, 'uwanews/_design/des/_view/getlinks')
    r = requests.get(end_point)
    r = r.json()
    t = []
    for item in r.get('rows'):
        t.append(item.get('value'))
    for i in list:
        # If item already in database, ignore it - if not, add analysis results to database
        if not i in t:
            data = alchemy.combined(url=i, extract=combined_operations)
            doc = database.create_document(data)
            if not doc.exists():
                return "Doc not created: " + jsonify(results=data)
    end_point = '{0}/{1}'.format(cl_url, 'uwanews/_design/des/_view/getlinks')
    r = requests.get(end_point)
    r = r.json()
    t = []
    for item in r.get('rows'):
        t.append(item.get('value'))
    return jsonify(results=t)

# Check how many calls left on AlchemyAPI
@app.route('/apikey')
def apiKey():
    return jsonify(alchemy_calls_left(api_key=api_key))

# Create a database in the Cloudant app
@app.route('/createdb/<db>')
def create_db(db):
    requests.put( cl_url + '/' + db, auth=auth )
    return 'Database %s created.' % db

# Get a pie chart of the total emotional analysis results from the entire database
@app.route('/getemotions.svg')
def GetEmotions():
    end_point = '{0}/{1}'.format(cl_url, 'uwanews/_design/des/_view/getemotions')
    r = requests.get(end_point)
    r = r.json()
    t = {}
    t['disgust'] = 0
    t['fear'] = 0
    t['joy'] = 0
    t['sadness'] = 0
    t['anger'] = 0
    # Add all the emotions
    for item1 in r.get('rows'):
        emotion = item1.get('value')
        t['disgust'] += float(emotion.get('disgust'))
        t['fear'] += float(emotion.get('fear'))
        t['joy'] += float(emotion.get('joy'))
        t['sadness'] += float(emotion.get('sadness'))
        t['anger'] += float(emotion.get('anger'))
    try:
        title = 'Key Emotions'
        pie_chart = pygal.Pie(title=title, style=s)
        for key in t:
            pie_chart.add(key, t[key])
        return pie_chart.render_response()
    except Exception as ex:
        template = "An exception of type {0} occured. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        return "1: " + message

# Get all the most relevant topics, and graph them
@app.route('/mostrelevant.svg')
def MostRelevant():
    try:
        end_point = '{0}/{1}'.format(cl_url, 'uwanews/_design/des/_view/getrelevance')
        r = requests.get(end_point)
        r = r.json()
        t = {}
        for item in r.get('rows'):
            if item.get('key') in t:
                t[item.get('key')] +=  float(item.get('value'))
            else:
                t[item.get('key')] =  float(item.get('value'))
        title = 'Most Relevant Topics'
    except Exception as ex:
        template = "An exception of type {0} occured. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        return "1: " + message
    try:
        # Add the relevance and the topics
        relevance =  [float(t[key]) for key in t]
        labels = ['%s' % str(i) for i in t]
        bar_chart =  pygal.Bar(title=title, style=s)
        bar_chart.x_labels = labels
        bar_chart.add('Relevance', relevance)
        return bar_chart.render_response()
    except Exception as ex:
        template = "An exception of type {0} occured. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        return "2: " + message

# Advanced search, where users put in JSON
@app.route('/advancedsearch')
def AdvancedSearch():
    form = JForm(request.form, csrf_enabled=False)
    if request.method == 'POST' or request.method=='GET':
        if form.validate() == False:
            return render_template('advancedsearch.html', form=form)
        else:
            return redirect(url_for('Advanced'), request=request)
    return render_template('advancedsearch.html', form=form)

# Process data from the advanced search
@app.route('/advanced')
def Advanced(request):
    url = request.form.get("text")
    j = json.loads(url)
    tofind = "{0}/{1}/_find/".format(cl_url, "uwanews")
    a = requests.post(tofind, json=j)
    a = a.json()
    return a
    # a = a['docs'][0]

# display results of all the documents
@app.route('/getstats')
def getHTML():
    html = """
                <div class='rightHalf'>
                <figure>
                 <embed type="image/svg+xml" src="{0}" />
                 </figure>
                 </div>
                 <div class='leftHalf'>
                 <figure>
                 <embed type="image/svg+xml" src="{1}" />
                 </figure>
                 </div>
                """.format(url_for('MostRelevant'), url_for('GetEmotions'))
    return render_template('layout.html', message=Markup(html))

# Run the app
port = os.getenv('PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port), debug=True)
