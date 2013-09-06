import flask, machine

def get(*args):
	return flask.render_template(
		"bitcoin/order.html", **machine.get(*args))
