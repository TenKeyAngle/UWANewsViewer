from watson_developer_cloud import AlchemyLanguageV1
from cloudant import cloudant
from cloudant.client import Cloudant
from cloudant.document import Document
from flask import jsonify
import json
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
end_point = '{0}/{1}'.format(cl_url, 'x/_all_docs')
#params = {'include_docs': 'true'}
r = requests.get(end_point)
print(r.json())
doc = my_database['1d8c54f34b43c94894f01744608dbf46']
#print(json.dumps(doc))
# Disconnect from the server
client.disconnect()