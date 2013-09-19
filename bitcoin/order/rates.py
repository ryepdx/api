import json, urllib2
from decimal import Decimal, getcontext, ROUND_UP, ROUND_DOWN

class WeightedRates(object):
	def __init__(self, margin):
		self.margin = Decimal(margin)

		try:
			with open("markets.json", "r") as handle:
				rawMarkets = handle.read()
		except:
			rawMarkets = urllib2.urlopen("http://api.bitcoincharts.com/v1/markets.json").read()
			with open("markets.json", "w") as handle:
				handle.write(rawMarkets)
		finally:
			markets = json.loads(rawMarkets)

		bitstamp = filter(lambda mkt: mkt["symbol"] == "bitstampUSD", markets)[0]
		self.ask = Decimal(bitstamp["ask"])
		self.bid = Decimal(bitstamp["bid"])

		#self.price = Decimal(json.loads(
		#	urllib2.urlopen("http://api.bitcoincharts.com/v1/weighted_prices.json").read()
		#)["USD"]["24h"])

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
	markets = urllib2.urlopen("http://api.bitcoincharts.com/v1/markets.json").read()
	with open("markets.json", "w") as handle:
		handle.write(markets)
