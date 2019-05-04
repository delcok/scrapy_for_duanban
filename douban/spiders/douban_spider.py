# -*- coding: utf-8 -*-
import scrapy
from douban.items import DoubanItem


class DoubanSpiderSpider(scrapy.Spider):
    #爬虫名字
    name = 'douban_spider'
    #允许的域名
    allowed_domains = ['movie.douban.com']
    #入口url
    start_urls = ['http://movie.douban.com/top250']

    def parse(self, response):
        movie_list = response.xpath("//div[@class='article']//ol[@class='grid_view']/li")
        for i in movie_list:
            douban_item = DoubanItem()
            douban_item['serial_number'] = i.xpath(".//div[@class='item']//em/text()").extract_first()
            douban_item['movie_name']=i.xpath(".//div[@class='info']/div[@class='hd']/a/span[1]/text()").extract_first()
            content = i.xpath(".//div[@class='info']//div[@class='bd']/p[1]/text()").extract()
            douban_item['star'] = i.xpath(".//span[@class='rating_num']/text()").extract_first()
            douban_item['evaluate'] = i.xpath(".//div[@class='star']//span[4]/text()").extract_first()
            douban_item['describe'] = i.xpath(".//p[@class='quote']/span/text()").extract_first()
            for i in content:
                content_s = "".join(i.split())
                douban_item['introduce'] = content_s
            # douban_item['star'] = i.xpath(".//span[@class='rating_num']/text()").extract_first()
            # print(douban_item['star'])
            # douban_item['evaluate'] = i.xpath(".//div[@class='star']//span[4]/text()").extract_first()
            # print(douban_item['evaluate'])
            # douban_item['describe'] = i.xpath(".//p[@class='quote']/span/text()").extract_first()
            # print(douban_item['describe'])
            yield  douban_item
        next_link = response.xpath("//span[@class='next']/link/@href").extract()
        if next_link:
            next_link = next_link[0]
            yield scrapy.Request("https://movie.douban.com/top250"+next_link,callback=self.parse)


