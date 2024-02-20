# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 19:23:01 2023

@author: HP
"""

import scrapy
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from scrapy.selector import Selector

class groww(scrapy.Spider):
    name="practice"
    start_urls=["https://groww.in/mutual-funds/collections/best-high-return","https://groww.in/mutual-funds/collections/best-sip-with-500","https://groww.in/mutual-funds/collections/best-tax-saving",
               "https://groww.in/markets/top-gainers?index=GIDXNIFTY100","https://groww.in/markets/top-losers?index=GIDXNIFTY100",
                "https://groww.in/stocks/filter?closePriceHigh=100000&closePriceLow=0&marketCapHigh=2000000&marketCapLow=0&page=0&size=15&sortType=ASC"]
    

    def parse(self,response):
        self.driver = webdriver.Chrome()  
        self.driver.get(response.url)
        for _ in range(5):  
            self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)

        
        self.driver.implicitly_wait(10)

        page_source = self.driver.page_source  
        selector = Selector(text=page_source)
        table = selector.css('td')
        url=response.url
        date=datetime.date.today()
        if 'mutual-funds' in url:
            fundInfo=table.css('div.cst14FundInfo')
            fundName=fundInfo.css('a::text').extract()
            fundReturns=table.css('td.cst14ColumnPadding::text').extract()
            fundReturns1Year=[]
            for i in range(0,len(fundReturns),2):
                fundReturns1Year.append(fundReturns[i])
            fundReturns3Year=[]
            for i in range(1,len(fundReturns),2):
                fundReturns3Year.append(fundReturns[i])
            fundReturns5 = response.xpath('//*[@id="root"]/div[2]/div[2]/div/div/div[1]/div[2]/table/tbody')
            fundReturns5Year=[]
            for row in fundReturns5.xpath('./tr'):
                fund_5_year_returns = row.xpath('./td[4]/text()').get()
                fundReturns5Year.append(fund_5_year_returns)
            if 'best-high-return' in url:
                Category='Best-high-return'
            if 'best-sip-with-500' in url:
                Category='Best-sip-with-500'
            if 'best-large-cap' in url:
                Category='Best-large-cap'
            if 'best-mid-cap' in url:
                Category='Best-mid-cap'
            if 'best-tax-saving' in url:
                Category='Best-tax-saving'
            if 'best-small-cap' in url:
                Category='Best-small-cap'
            Type="Mutual-Funds"
            for i in range(len(fundName)):
                yield{"FundName":fundName[i],"1Y":fundReturns1Year[i],"3Y":fundReturns3Year[i],"5Y":fundReturns5Year[i],"Date":str(date),"Category":Category,"Type":Type}
        elif 'stocks/filter' in url:
            stockName=selector.css('.st76SymbolName::text').extract()
            print(stockName)
            stockValue=selector.css('.bodyRegular14::text').extract()
            marketValue=selector.css('.bodyMedium14::text').extract()
            marketValueList=[]
            for value in marketValue:
                try:
                    value_number = value.replace(",","")
                    float_number=float(value_number.replace("₹",""))
                    marketValueList.append(float_number)  
                except ValueError:
                    pass
            print(marketValueList)
            stockValueList=[]
            for value in stockValue:
                try:
                    value_number = value.replace(",","")
                    float_number=float(value_number.replace("₹",""))
                    stockValueList.append(float_number)  
                except ValueError:
                    pass
            closePrice=[]
            for i in range(0,len(stockValueList),2):
                closePrice.append(stockValueList[i])
            marketCap=[]
            for i in range(1,len(stockValueList),2):
                marketCap.append(stockValueList[i])
            for k in range(len(stockName)):
                yield{"StockName":stockName[k],"Market Value":marketValueList[k],"Close Price":closePrice[k],"Market Cap":marketCap[k],"Category":"All-Stocks","Type":"Stocks","Date":date}
            for page_number in range(1,10):
                next_page_url = f"https://groww.in/stocks/filter?closePriceHigh=100000&closePriceLow=0&marketCapHigh=2000000&marketCapLow=0&page={page_number}&size=15&sortType=ASC"
                yield scrapy.Request(url=next_page_url, callback=self.parse)
        
        else:
            tableStock=selector.css('table.tb10Table')
            tr=tableStock.css('tr')
            stockName=tr.css('a::text').extract()
            stockValue=tr.css('td.bodyMedium14::text').extract()
            WValue=tr.css('.tb10Td::text').extract()
            WLow=[]
            for i in range(0,len(WValue),2):
                WLow.append(WValue[i])
            WHigh=[]
            for i in range(1,len(WValue),2):
                WHigh.append(WValue[i])
            Type="Stocks"
            if 'top-gainers' in url:
                Category='Top-gainers'
            if 'top-losers' in url:
                Category='Top-losers'
            if 'top-volume' in url:
                Category='Top-volume'
            
            for k in range(len(stockName)):
                yield{"StockName":stockName[k],"Market Value":stockValue[k],"52W Low":WLow[k],"52W High":WHigh[k],"Category":Category,"Type":Type,"Date":date}
