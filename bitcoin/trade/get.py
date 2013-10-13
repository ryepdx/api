import flask, rates, settings
from inventory import Inventory

def machine(*args):
	prices = rates.WeightedRates(settings.BTC_MARGIN)
	inventory = Inventory(
		address = settings.INVENTORY_ADDRESS, user_agent = settings.USER_AGENT
	)
	
	reply = { "inventory": str(inventory.value) }
	
	if (inventory.value <= settings.BUY_THRESHOLD):
		reply["buy_price"] = str(prices.buy)
		reply["mailing_address"] = settings.BTC_MAILING_ADDRESS
	
	if (inventory.value >= settings.SELL_THRESHOLD):
		reply["sell_price"] = str(prices.sell)
		reply["btc_address"] = settings.INVENTORY_ADDRESS
	
	return reply

def human(*args):
	params = machine(*args)
	params["order_stylesheet"] = flask.url_for('static', filename='bitcoin/order.css')
	params["scripts"] = [
		flask.url_for('static', filename='bitcoin/order.js'),
		flask.url_for('static', filename='big.min.js'),
		flask.url_for('static', filename='sjcl.js')
	]

	return flask.render_template(
		"bitcoin/order.html", **params)

