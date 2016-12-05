import blackmarket as Blackmarket
import time


bm = Blackmarket.Blackmarket()

while True:
	for item in bm.fetch():
		print (item.name, item.item_id)
	time.sleep(1)
