# -*- coding: utf-8 -*-
"""
Created on Fri Aug 25 14:56:35 2023

@author: HP
"""

import scrapy
from ..items import Lab1Item

class QuoteSpider(scrapy.Spider):
    name = 'Lab1'
    start_urls=["https://quotes.toscrape.com/"]
    #start_urls=["https://groww.in/mutual-funds/user/explore"]
    
    def parse(self,response):
        #title=response.css('title::text').extract()
        all_div_quotes=response.css('div.quote')
        title=all_div_quotes.css('span.text::text').extract()
        author=all_div_quotes.css('.author::text').extract()
        tag=all_div_quotes.css('.tag::text').extract()
        for i in range(len(title)):
                yield{'title':title[i],'author':author[i],'tag':tag[i]}
                
    """def parse(self,response):
        items=Lab1Item()
        all_div_quotes=response.css('div.quote')
        for quotes in all_div_quotes:
            title=all_div_quotes.css('span.text::text').extract()
            author=all_div_quotes.css('.author::text').extract()
            tag=all_div_quotes.css('.tag::text').extract()
            items['title']=title
            items['author']=author
            items['tag']=tag
                
        yield items"""
        
    """def parse(self, response):

        title = response.css('.mfc024TruncateLabel::text').extract()

        yield{'titletest':title}"""
            
                
        
                
        