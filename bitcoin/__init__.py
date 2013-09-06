import flask

def human():
	return flask.render_template("bitcoin.html", **machine())

def machine():
	return { "donation_address": "1HXERr3GXcKDMs1J5dM59GWL5ZfWBxNLw9" }
