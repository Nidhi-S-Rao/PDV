# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
#def process_item(self, item, spider):
#return item
import sqlite3
from itemadapter import ItemAdapter


class Lab1Pipeline:
    def __init__(self):
        self.create_connection()
        self.create_table()
    def create_connection(self):
        self.conn=sqlite3.connect("myquotes.db")
        self.curr=self.conn.cursor()
    def create_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS quotes_tb""")
        self.curr.execute("""Create table quotes_tb(title varchar(45),author varchar(45), tag text)""")
    def process_item(self,item,spider):
        self.store_db(item)
        return item
    def store_db(self,item):
        self.curr.execute("""Insert into quotes_tb values(?,?,?)""",
		(
		item['title'],
		item['author'],
		item['tag']))
        self.conn.commit()
