import scrapy
import urllib2
import urllib
from scrapy.spiders import BaseSpider
from scrapy.selector import Selector
from scrapy.http.request import Request
from scrapy.http.response import Response
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
import re
import csv
class Flipkart(scrapy.Spider):
    global flag
    search_q = raw_input("Enter what you want to search with quotation:")
    search_q= search_q.replace(" ", "+")
    search_url="http://www.flipkart.com/search?q="+search_q
    print search_url
    name = "flipkart"
    allowed_domains = ['flipkart.com']
    start_urls = [search_url]
    flag=0
    fo=open("reviews.csv","w+")
    fo.write("Rating,Date,Review\n")
    fo.close()
    def parse(self, response):
        hxs=Selector(response)
        links = hxs.xpath(".//div[@class='pu-details lastUnit']/div[@class='pu-title fk-font-12']/a/@href").extract()
        link="http://flipkart.com"+links[0]
        request = scrapy.Request(link,callback=self.parse_review)
        yield request
    def parse_review(self, response):
        hxs = Selector(response)
        newlinks= hxs.xpath(".//div[@class='subLine']/p[@class='subText']/a/@href").extract()
        newlink="http://flipkart.com"+newlinks[0]
        request = scrapy.Request(newlink,callback=self.parse_review2)
        yield request

    def parse_review2(self, response):
        hxs = Selector(response)
        review_elements=hxs.xpath(".//span[@class='review-text']").extract()
        review_rating=hxs.xpath(".//div[@class='line']/div[@class='fk-stars']/@title").extract()
        review_date=hxs.xpath(".//div[@class='unit size1of5 section1']/div[@class='date line fk-font-small']/text()").extract()
        tmp1=0

        for review_element in review_elements:
            review_element=review_element.replace("<br>", "")
            review_element=review_element.replace('<span class="review-text">', "")
            review_element=review_element.replace("</span>", "")
            review_element=(review_element).replace("\n", "")
            review_element=(review_element).replace('"', '\\"')
            review_element=review_element.encode('utf-8')
            fo=open("reviews.csv","a")
            fo.write(review_rating[tmp1]+",")
            fo.write(review_date[tmp1].replace("\n", "")+',"')
            fo.write(review_element)
            fo.write('"\n')
            #fo.close()
            fo.close()
            tmp1=tmp1+1

        next_page_link = hxs.xpath(".//a[@class='nav_bar_next_prev']/@href").extract()
        k=len(next_page_link)-1

        next_page_go_link= "http://flipkart.com"+next_page_link[k]
        if next_page_go_link: # check if there is a next page at all
            yield Request(next_page_go_link, callback=self.parse_review2)
