from time import sleep

import requests
import sys
from cloudant import Cloudant
from scrapy import crawler
from scrapy.exceptions import DropItem, CloseSpider
from watson_developer_cloud import AlchemyLanguageV1

from helper import alchemy_calls_left
from welcome import api_key, cl_url, cl_username, cl_password


class URLPipeline(object):

    def open_spider(self, spider):
        self.alchemy = alchemy = AlchemyLanguageV1(api_key=api_key)
        client = Cloudant(cl_username, cl_password, url=cl_url)
        client.connect()
        self.database = client['uwanews']
        end_point = '{0}/{1}'.format(cl_url, 'uwanews/_design/des/_view/getlinks')
        r = requests.get(end_point)
        r = r.json()
        self.t = []
        for item in r.get('rows'):
            self.t.append(item.get('value'))

    def process_item(self, item, spider):
        combined_operations = ['title', 'authors', 'pub-date', 'entities', 'keywords',  'taxonomy', 'relations', 'concepts', 'doc-emotion']
        al = alchemy_calls_left(api_key=api_key)
        if not al['consumedDailyTransactions'] < al['dailyTransactionLimit']:
            # If limit surpassed, return a string letting user know
            str = 'AlchemyAPI calls depleted for today: consumed.{}'.format(al['consumedDailyTransactions'])
            crawler.engine.close_spider(spider, 'AlchemyAPI used too much')
            sys.exit()
            raise CloseSpider(str)
        if not item['url'] == None:
            # If item already in database, ignore it - if not, add analysis results to database
            if not item['url'] in self.t:
                data = self.alchemy.combined(url=item, extract=combined_operations)
                doc = self.database.create_document(data)
                if not doc.exists():
                    print("Doc not created: {0}".format(item['url']))
            return item
        else:
            raise DropItem("Url is " % item['url'])


