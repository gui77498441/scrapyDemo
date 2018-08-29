from ..items import ScrapydemoItem
import re
import scrapy
from scrapy.http import Request,response
import io

class mySpider(scrapy.Spider):
    name = 'scrapyDemo'  #entrypoint.py中第三个参数
    baseUrl = 'https://read.douban.com/kind/190?'

    #生成爬取链接
    def start_requests(self):
        for i in range(0,1,1):
            url = self.baseUrl + 'start=' +str(i)
            yield Request(url,self.parse)
    

    #解析器
    def parse(self,response):
        text = response.text
        open('result.html','w').write(text)

