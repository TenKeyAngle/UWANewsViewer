import os
import json
import requests
from flask import Flask

app = Flask(__name__)

app.config.update(
    DEBUG=True,
)

@app.route('/')
def welcome():
    return 'Welcome to flask and Cloudant on Bluemix.'

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

port = os.getenv('VCAP_APP_PORT', '5000')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(port))