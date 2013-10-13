import flask

def machine(*args):
	return {
		"donation_address": "1HXERr3GXcKDMs1J5dM59GWL5ZfWBxNLw9"
	}

def human(*args):
	return flask.render_template("bitcoin.html", **(machine()))
