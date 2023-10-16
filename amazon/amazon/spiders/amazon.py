# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 23:46:30 2023

@author: HP
"""

import scrapy
from ..items import AmazonItem

class Amazon(scrapy.Spider):
    name="amazon"
    start_urls=["https://www.amazon.in/s?k=bluetooth+headphones+amazon&adgrpid=63397363140&ext_vrnc=hi&hvadid=590652605668&hvdev=c&hvlocphy=9147869&hvnetw=g&hvqmt=e&hvrand=3498836193702863468&hvtargid=kwd-303902366796&hydadcr=24535_2265404&tag=googinhydr1-21&ref=pd_sl_1fhx1hnn3f_e"]
    page_number=1
    def parse(self,response):
        names=response.css(".a-text-normal::text").extract()
        cleaned_names=[]
        prices=response.css(".a-price-whole::text").extract()
        print(prices)
        for name in names:
            if name!=' ':
                if '\n' not in name:
                    cleaned_names.append(name)
        for i in range(len(cleaned_names)):
            yield{"name":cleaned_names[i],"price":prices[i]}

        next_page_button = response.css(".sg-row")
        if next_page_button and self.page_number<=9:
            self.page_number += 1
            next_page_url = f"https://www.amazon.in/s?k=bluetooth+headphones+amazon&adgrpid=63397363140&ext_vrnc=hi&hvadid=590652605668&hvdev=c&hvlocphy=9147869&hvnetw=g&hvqmt=e&hvrand=3498836193702863468&hvtargid=kwd-303902366796&hydadcr=24535_2265404&tag=googinhydr1-21&ref=pd_sl_1fhx1hnn3f_e&page={self.page_number}"
            yield scrapy.Request(url=next_page_url, callback=self.parse)
        
        
        
        
        