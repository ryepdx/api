import os, json, urllib2
from decimal import Decimal, getcontext, ROUND_UP, ROUND_DOWN

class WeightedRates(object):
	def __init__(self, margin):
		self.margin = Decimal(margin)
		curdir = os.path.dirname(os.path.realpath(__file__))

		try:
			with open(curdir + "/markets.json", "r") as handle:
				rawMarkets = handle.read()
		except:
			rawMarkets = urllib2.urlopen("http://api.bitcoincharts.com/v1/markets.json").read()
			with open(curdir + "/markets.json", "w") as handle:
				handle.write(rawMarkets)
		finally:
			markets = json.loads(rawMarkets)

		bitstamp = filter(lambda mkt: mkt["symbol"] == "bitstampUSD", markets)[0]
		self.ask = Decimal(str(bitstamp["ask"]))
		self.bid = Decimal(str(bitstamp["bid"]))

	@property
	def buy(self):
		return (self.bid - self.bid * self.margin).quantize(
			Decimal('.01'), rounding = ROUND_DOWN
		)

	@property
	def sell(self):
		return (self.ask + self.ask * self.margin).quantize(
			Decimal('.01'), rounding = ROUND_UP
		)

if __name__ == "__main__":
	curdir = os.path.dirname(os.path.realpath(__file__))
	markets = urllib2.urlopen("http://api.bitcoincharts.com/v1/markets.json").read()
	with open(curdir + "/markets.json", "w") as handle:
		handle.write(markets)
