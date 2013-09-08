import json, urllib2
from decimal import Decimal, getcontext, ROUND_UP, ROUND_DOWN

class WeightedRates(object):
	def __init__(self, margin):
		self.margin = Decimal(margin)
		self.price = Decimal(json.loads(
			urllib2.urlopen("http://api.bitcoincharts.com/v1/weighted_prices.json").read()
		)["USD"]["24h"])

	@property
	def buy(self):
		return (self.price - self.price * self.margin).quantize(
			Decimal('.01'), rounding = ROUND_DOWN
		)

	@property
	def sell(self):
		return (self.price + self.price * self.margin).quantize(
			Decimal('.01'), rounding = ROUND_UP
		)
