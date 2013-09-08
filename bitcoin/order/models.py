from app import db
from _wrappers import JsonGet, HtmlGet
import datetime

class Order(db.Model):
	token = db.Column(db.String(64), primary_key = True)
	seed = db.Column(db.Integer)
	rand = db.Column(db.Float)
	created = db.Column(db.DateTime, default=datetime.datetime.now)
	usd = db.Column(db.Float)
	btc = db.Column(db.Float)
	price = db.Column(db.Float)
	ip_address = db.Column(db.String(39))
	public_attrs = ["token", "created", "usd", "btc", "price"]

	def __init__(self, token, seed, rand, usd, btc, price, ip_address):
		self.token = token
		self.seed = seed
		self.rand = rand
		self.usd = usd
		self.btc = btc
		self.price = price
		self.ip_address = ip_address

	def __iter__(self):
		return self

	def next(self):
		if not hasattr(self, "_index"):
			self._index = 0
	
		if self._index == len(self.public_attrs):
			raise StopIteration
	
		attr =  self.public_attrs[self._index]
		self._index += 1
		return (attr, getattr(self, attr))

	@property
	def machine(self):
		return JsonGet(self)

	@property
	def human(self):
		return HtmlGet(self)
