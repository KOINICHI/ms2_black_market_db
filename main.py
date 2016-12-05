import blackmarket as Blackmarket
import time


bm = Blackmarket.Blackmarket()

while True:
	for item in bm.fetch():
		if item.type != 'cancelled':
			print (item.name, item.price)
	time.sleep(1)
