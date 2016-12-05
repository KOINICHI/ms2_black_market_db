from datetime import datetime
import re

class Transaction:
	def __init__(self, raw_item):
		self.type = raw_item['action']
		if self.type == "메소에 매물로 나와!":
			self.type = 'listed'
		elif self.type == "메소에 팔려!":
			self.type = 'sold'
		elif self.type == "판매 취소!":
			self.type = 'cancelled'

		if self.type in ['listed', 'sold']:
			self.price = int(re.sub('[^0-9]', '', raw_item['price']))

		self.name = re.sub('<[^<]+?>', '', raw_item['item_name']) 

		self.item_id = int(re.sub('[^0-9]', '', raw_item['item_data']))

		self.timestamp = float(re.sub('[^(0-9|\.)]', '', raw_item['time']))

		self.time = datetime.fromtimestamp(self.timestamp)
