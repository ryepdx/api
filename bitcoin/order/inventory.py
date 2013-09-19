import json, urllib2
from decimal import Decimal

def _addressInfoFromInternet(address, user_agent):
	return urllib2.urlopen(
		urllib2.Request("http://blockchain.info/address/%s?format=json" % address,
			headers = { "User-Agent": user_agent })
	).read()

class Inventory(object):
	def __init__(self, address = None, user_agent = None):
		self.address = address
		self.user_agent = user_agent
		
		try:
			with open("inventory.json", "r") as handle:
				addrInfo = json.loads(handle.read())
		except:
			rawAddrInfo = _addressInfoFromInternet(self.address, self.user_agent)
			
			try:
				with open("inventory.json", "w") as handle:
					handle.write(rawAddrInfo)
			finally:
				addrInfo = json.loads(rawAddrInfo)
		self.value = Decimal(addrInfo['final_balance']) / Decimal(100000000)
	
	def __str__(self):
		return str(self.value)

if __name__ == "__main__":
	import sys, os
	curdir = os.path.dirname(os.path.realpath(__file__))
	with open(curdir + "/inventory.json", "w") as handle:
		handle.write(_addressInfoFromInternet(sys.argv[1], sys.argv[2]))
