from app import db
from cyborg import DefaultGet
import datetime, decimal, flask, settings

class OrderGet(DefaultGet):
	def __init__(self, order):
		self.order = order
		super(OrderGet, self).__init__(order)

	def human(self, *args):
		params = {
			"order_token": self.order.token, 
			"mailing_address": settings.BTC_MAILING_ADDRESS,
			"usd": decimal.Decimal(str(self.order.usd)
				).quantize(decimal.Decimal('0.01'))
		}
		params["order_stylesheet"] = flask.url_for('static', filename='bitcoin/order.css')
		return flask.render_template("bitcoin/ordered.html", **params)
		
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
	def get(self):
		return OrderGet(self)
