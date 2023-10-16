# -*- coding: utf-8 -*-
"""
Created on Sun Oct 15 10:43:42 2023

@author: HP
"""

import scrapy
from ..items import MeeshoItem


class Meesho(scrapy.Spider):
    name="meesho"
    start_urls=["https://www.meesho.com/dresses-women/pl/3j3","https://www.meesho.com/casual-shoes-women/pl/3t2",
                "https://www.meesho.com/jhumkas/pl/3lr"]
        
    def parse(self,response):
        
        name=response.css('.ejhQZU::text').extract()
        prices=response.css('.dydzqM::text,.hMaXQw::text').extract()
        cleaned_prices=[]
        for price in prices:
            cleaned_price = price.strip('₹ ').replace(',', '')
            if cleaned_price.isnumeric():
                cleaned_prices.append(int(cleaned_price))
        for i in range(len(name)):
            yield{"name":name[i],"price":cleaned_prices[i]}
        