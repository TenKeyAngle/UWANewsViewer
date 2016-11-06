from watson_developer_cloud import AlchemyLanguageV1
from cloudant import cloudant
from cloudant.client import Cloudant
from cloudant.document import Document

cl_username = "1a818337-f029-449a-8a03-d34f30877d1d-bluemix"
cl_password = "b20bcbf26bac5fa4ed56df09b07755ac1d8ccf6e3d3ad1177902957c1ca192c0",
url         = "https://1a818337-f029-449a-8a03-d34f30877d1d-bluemix:b20bcbf26bac5fa4ed56df09b07755ac1d8ccf6e3d3ad1177902957c1ca192c0@1a818337-f029-449a-8a03-d34f30877d1d-bluemix.cloudant.com"

client = Cloudant(cl_username, cl_password, url=url)



# Connect to the server
client.connect()

# Perform client tasks...
session = client.session()
my_database = client['x']

if my_database.exists():
    print('SUCCESS!')

# Disconnect from the server
client.disconnect()