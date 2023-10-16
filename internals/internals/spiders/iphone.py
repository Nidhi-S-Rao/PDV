# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 14:05:01 2023

@author: HP
"""
import scrapy
class flipkartScraper(scrapy.Spider):
    name="internals"
    start_urls=["https://www.flipkart.com/mobiles/apple~brand/pr?sid=tyy,4io"]
    def parse(self,response):
        iphone=response.css('div._2kHMtA')
        name=iphone.css('._4rR01T::text').extract()
        price=iphone.css('._1_WHN1::text').extract()
        rom=iphone.css('.rgWa7D::text').extract()
        rom_string=''.join(rom)
        rom_list=rom_string.split('|')
        for i in range(len(name)):
            yield{"name":name[i].split('(')[0],"color":(name[i].split('(')[1]).split(',')[0],"price":price[i],"RAM":((name[i].split('(')[1]).split(',')[1]).split(')')[0],"Features":rom_list[i]}
