import app, flask, rates, hashlib, models, random, settings, time
from decimal import Decimal, ROUND_DOWN

def machine(request):
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
		"btc_ordered": str(btc),
		"btc_price": str(price),
		"usd_to_send": str(usd),
		"mailing_address": settings.BTC_MAILING_ADDRESS
	}

def human(*args):
	order = machine(*args)
	return flask.redirect("bitcoin/order/%s.html" % order["order_token"])
