class URLPipeline(object):
    def open_spider(self, spider):
        self.file = open('items/news2.csv', 'w')

    def close_spider(self, spider):
        self.file.close()


    def process_item(self, item, spider):
        if not item['url'] == None:
            self.file.write(item)
            return item
