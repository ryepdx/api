import flask, machine

def get(*args):
	params = machine.get(*args)
	params["order_stylesheet"] = flask.url_for('static', filename='bitcoin/order.css')
	params["scripts"] = [
		flask.url_for('static', filename='bitcoin/order.js'),
		flask.url_for('static', filename='big.min.js'),
		flask.url_for('static', filename='sjcl.js')
	]

	return flask.render_template(
		"bitcoin/order.html", **params)

def post(*args):
	order = machine.post(*args)
	return flask.redirect("bitcoin/order/%s.html" % order["order_token"])
