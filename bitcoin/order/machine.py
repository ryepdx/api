import app, flask, rates, hashlib, models, random, settings, time
from decimal import Decimal, ROUND_DOWN
from inventory import Inventory

def get(*args):
	prices = rates.WeightedRates(settings.BTC_MARGIN)
	inventory = Inventory(
		address = settings.INVENTORY_ADDRESS, user_agent = settings.USER_AGENT
	)
	
	reply = { "inventory": inventory }
	
	if (inventory.value <= settings.BUY_THRESHOLD):
		reply["buy_price"] = prices.buy
		reply["mailing_address"] = settings.BTC_MAILING_ADDRESS
	
	if (inventory.value >= settings.SELL_THRESHOLD):
		reply["sell_price"] = prices.sell
		reply["btc_address"] = settings.INVENTORY_ADDRESS
	
	return reply

def post(request):
	# Generate a unique token for this order.
	curr_time = time.time()
	seed = request.form["seed"]
	prices = rates.WeightedRates(settings.BTC_MARGIN)
	price = prices.sell
	rand = random.SystemRandom(seed + str(curr_time) + str(price)).random()
	token = hashlib.sha256(str(rand)).hexdigest().upper()[0:9]
	usd = Decimal(request.form["usd"])	
	btc = (usd / price).quantize(
		Decimal('.00000001'), rounding = ROUND_DOWN)

	# Save the order.
	app.db.session.add(models.Order(
		token, seed, rand, usd, btc, price, request.remote_addr
	))
	app.db.session.commit()

	# Return amount bought.
	return {
		"order_token": token,
		"btc_ordered": btc,
		"btc_price": price,
		"usd_to_send": usd,
		"mailing_address": settings.BTC_MAILING_ADDRESS
	}
