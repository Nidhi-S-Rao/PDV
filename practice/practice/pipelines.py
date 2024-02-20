# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import sys
sys.path.append("C:/Users/HP/Desktop/practice/practice")
import mysql.connector
from settings import DATABASE_SETTINGS



class PracticePipeline:
    def __init__(self):
        self.create_connection()
        #self.create_table()
    def create_connection(self):
        self.conn=mysql.connector.connect(**DATABASE_SETTINGS)
        self.curr=self.conn.cursor()
    def create_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS MutualFunds""")
        self.curr.execute("""Create table MutualFunds(FundName varchar(100),Returns1Y varchar(15), Returns3Y varchar(15),Returns5Y varchar(15), Date date, Category varchar(25),Type varchar(20))""")
        self.curr.execute("""DROP TABLE IF EXISTS Stocks""")
        self.curr.execute("""Create table Stocks(StockName varchar(100),MarketValue varchar(15), Low varchar(15),High varchar(15), Date date, Category varchar(25),Type varchar(20))""")
        self.curr.execute("""DROP TABLE IF EXISTS AllStocks""")
        self.curr.execute("""Create table AllStocks(StockName varchar(100),MarketValue varchar(15), ClosePrice varchar(15),MarketCap varchar(15), Date date, Category varchar(25),Type varchar(20))""")
    def process_item(self,item,spider):
        if 'FundName' in item:
            self.store_mutual_funds(item)
        if 'Market Cap' in item:
            self.store_all_stocks(item)
        if '52W Low' in item:
            self.store_stocks(item)
        return item
    def store_mutual_funds(self,item):
        self.curr.execute("""Insert into MutualFunds values(%s, %s, %s, %s, %s, %s, %s)""",
		(
		item['FundName'],
		item['1Y'],
		item['3Y'],
        item['5Y'],
        item['Date'],
        item['Category'],
        item['Type']))
        self.conn.commit()
    def store_all_stocks(self,item):
        print("All")
        self.curr.execute("""Insert into AllStocks values(%s, %s, %s, %s, %s, %s, %s)""",
		(
		item['StockName'],
		item['Market Value'],
		item['Close Price'],
        item['Market Cap'],
        item['Date'],
        item['Category'],
        item['Type']))
        self.conn.commit()
    def store_stocks(self,item):
        print("Stocks")
        self.curr.execute("""Insert into Stocks values(%s, %s, %s, %s, %s, %s, %s)""",
		(
		item['StockName'],
		item['Market Value'],
		item['52W Low'],
        item['52W High'],
        item['Date'],
        item['Category'],
        item['Type']))
        self.conn.commit()

