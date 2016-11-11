import wtforms
from flask import url_for
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, validators
import requests
import csv

# Helper methods and classes for the main application

# Forms used in the application

# Form for searching by URL and by keywords
class LinkForm(FlaskForm):
    name = StringField('Search News', validators=[validators.input_required()], default='     Search by URL or by keyword')

# Form search for JSON
class JForm(FlaskForm):
    str = '{ "selector" : { "url" : "http://www.news.uwa.edu.au/201611049179/aboriginal-people-inhabited-was-mid-west' \
          '-coast-much-earlier-previously-thought" } }'
    text = TextAreaField('Search by JSON', validators=[validators.input_required()], default=str)

# Function to determine how many AlchemyAPI calls are left
# Gotten from https://gist.github.com/ianozsvald/4464247
def alchemy_calls_left(api_key):
    # This URL tells us how many calls we have left in a day
    URL = "http://access.alchemyapi.com/calls/info/GetAPIKeyInfo?apikey={}&outputMode=json".format(api_key)
    # call AlchemyAPI, ask for JSON response
    response = requests.get(URL)
    calls_left = response.json()
    return calls_left

# Formats the details for one document - prints out emotions, concepts and keywords
def getDocDeets(json):
    html =  '<h1 style="margin: 2em 2em 0 2em; text-align: center">Detailed View</h1>'
    html +="<table class='results'>"
    if 'title' in json:
        html+= "<tr><td colspan='3' id='title'>{}</td></tr>".format(str(json['title']))
    if 'url' in json:
        html+= "<tr><td colspan='3' id='url'><a href='{}'>{}</a></td></tr>".format(json['url'], json['url'])
    if 'publicationDate' in json:
        date = json['publicationDate']['date']
        year = date[:4]
        date = date[4:8]
        month = date[:2]
        date = date[2:4]
        day = date
        html+="<tr><td colspan='2' id='date'>{0}/{1}/{2}</td></tr>".format(day, month, year)
    if 'docEmotions' in json:
        emotes = json['docEmotions']
        html += "<tr><td colspan='3' id='emotes'>Doc Emotions:</td></tr>"
        for key in emotes:
            html += '<tr><td>'
            html += key
            html += '</td><td colspan="2">'
            html += emotes[key]
            html += '</td><td></td></tr>'
    if 'concepts' in json:
        concepts = json['concepts']
        html += "<tr><td colspan='3' id='concepts'>Concepts:</td></tr>"
        for concept in concepts:
            html += '<tr><td><a href="{0}">'.format(url_for('SearchDB', word=concept['text']))
            html += concept['text']
            html += '</a></td><td colspan="2">'
            html += concept['relevance']
            html += '</td></tr>'
    if 'keywords' in json:
        keywords = json['keywords']
        html += "<tr><td colspan='3' id='concepts'>"
        for keyword in keywords:
            html += '<tr><td><a href="{0}">'.format(url_for('SearchDB', word=keyword['text']))
            html += keyword['text']
            html += '</a></td><td colspan="2">'
            html += keyword['relevance']
            html += '</td></tr>'
    html += "</table>"
    return html

# Lays out search results - prints link and title
def getSearchResults(json):
    html =  '<h1 style="margin: 2em 2em 0 2em; text-align: center">Results View</h1>'
    html += "<table class='results' style='margin-top: 0'>"
    for item in json:
        html += "<tr><td>{0}</td></tr>".format(item['title'])
        html += "<tr style='margin-bottom:2em'><td><a href='{0}'>{1}</a></td></tr>".format(item['url'], item['url'])
    html += "</table>"
    return html

# cleans the CSV file from the scraper
def cleanCSV():
    f = open('items/news.csv', 'r+')
    output = open('items/news1.csv', 'w')
    reader = csv.reader(f)
    writer = csv.writer(output)
    for row in reader:
        if row[0] != 'url' and row[0] != '':
            # reader.deleterow(row)
            writer.writerow(row)
    f.close()
    output.close()

def appendCSV():
    f = open('items/news1.csv', 'r+')
    writer = csv.writer(f)
    writer.writerow(['Does', 'work?'])

#l = alchemy_calls_left(api_key='6026adae6314a2a74df3c7a23a8e99d7f6e20c28')
cl_url  = "https://1a818337-f029-449a-8a03-d34f30877d1d-bluemix:b20bcbf26bac5fa4ed56df09b07755ac1d8ccf6e3d3ad1177902957c1ca192c0@1a818337-f029-449a-8a03-d34f30877d1d-bluemix.cloudant.com"


j = {
    "selector": {
        "url": "http://www.news.uwa.edu.au/201611049179/aboriginal-people-inhabited-was-mid-west-coast-much-earlier-previously-thought"
    }
}
tofind = "{0}/{1}/_find/".format(cl_url, "uwanews")
#cleanCSV()
#appendCSV()
#a = requests.post(tofind, json=j)
#a = a.json()
#a = a['docs'][0]
#print(getHTML(json=a))