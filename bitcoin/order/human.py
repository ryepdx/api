import flask, machine

def get(*args):
	return flask.render_template(
		"bitcoin/order.html", **machine.get(*args))

def post(*args):
	return flask.render_template(
		"bitcoin/ordered.html", **machine.post(*args))
