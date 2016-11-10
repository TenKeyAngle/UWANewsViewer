import scrapy
import csv
import sys
from scrapy.crawler import CrawlerProcess

class NewsSpider(scrapy.Spider):
    name = 'newsspider'
    start_urls = ['http://www.news.uwa.edu.au/']
    list = []
    def parse(self, response):
        f = open('news.csv', 'rb')
        last = ""
        try:
            reader = csv.reader(f)
            rownum = 0
            for row in reader:
                if rownum == 3:
                    last = row[0]
                    break
                rownum += 1
        finally:
            f.close()
        for title in response.css('h3'):
            current = title.css('a ::attr(href)').extract_first()
            if current == last:
                print(current)
                return
            yield({'url' : current,
                   'title': title.css('a ::text').extract_first()})

        pages = response.css('a.active ::attr(href)').extract()
        next_page = 0
        if len(pages) == 10:
            next_page = pages[8]
        else:
            next_page = pages[10]
        if next_page != 0:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)
 #       return list
    
#process = CrawlerProcess({
#    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1'
#})

#process.crawl(BlogSpider)
#process.start()

