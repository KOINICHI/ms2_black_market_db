import requests
from datetime import datetime, timedelta

import json
import re
import sqlite3

import transaction as Transaction

class Blackmarket:
	maview_url = 'http://maview.nexon.com'
	headers = {
		'Accept' : 'application/json, text/javascript, */*; q=0.01',
		'Accept-Encoding' : 'gzip, deflate, sdch',
		'Accept-Language' : 'en-US,en;q=0.8,ja;q=0.6,ko;q=0.4',
		'Connection' : 'keep-alive',
		'DNT' : '1',
		'Host' : 'maview.nexon.com',
		'Referer' : 'http://maview.nexon.com/',
		'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
		'X-Requested-With' : 'XMLHttpRequest',
		'Cookie': 'PCID=14691493664274388441092; A2SK=act05:12470452538023508555; GGAN=0; CULTURE=ko-KR; IL=; NXCH=; IM=0; RDB=; NPP=; ENC=; NXMP=; isCafe=false; A2SR=http%253A%252F%252Fmaview.nexon.com%252F%3A1472925224173%3A0; isUseMKDPlus=0_0_0_0; NXGID=85318F45DF184B93A7F62FE66AA4671C; NXLW=SID=F6FA324AB987C7F937C106062A6DA4CE&PTC=http:&DOM=maview.nexon.com&ID=&CP=; NXPID=7238769033DD867EF5C670E6A29C4922; _ga=GA1.2.79577093.1469149367; HENC=; IsMobile=; TweetsSearchTime=' + str(datetime.now())[:-3]
	}

	def __init__(self):
		self.last_updated = datetime.now().timestamp()
		self.db = sqlite3.connect('blackmarket.db')

	def fetch(self):
		while True:
			try:
				res = requests.get(Blackmarket.maview_url + '/Now/GetMessageMarket', \
									data = {'_': str(int(self.last_updated * 1000))}, \
									headers = Blackmarket.headers, \
									timeout = 0.5)
				data = res.content.decode('utf-8')
			except:
				data = '[]'
			break
			
		data = json.loads(data)
		data = [Transaction.Transaction(x) for x in data]
		new_time = self.last_updated
		if len(data) > 0:
			new_time = data[-1].timestamp
		data = [x for x in data if x.timestamp > self.last_updated]
		self.last_updated = new_time

		for item in data:
			self.addItemToDB(item.item_id, item.name)
		return data

	def addItemToDB(self, item_id, name):
		cursor = self.db.cursor()
		cmd = """BEGIN
					IF NOT EXISTS (SELECT * FROM Items WHERE Id={0})
					BEGIN
						INSERT INTO Items VALUES ({0}, '{1}')
					END
				END""".format(item_id, name)
		cursor.execute(cmd)
		self.db.commit()

	def getItemById(self, item_id):
		curosr = self.db.cursor()
		cmd = "SELECT * FROM Items WHERE ID={0}".format(item_id)
		cursor.execute(cmd)
		return cursor.fetchone()
