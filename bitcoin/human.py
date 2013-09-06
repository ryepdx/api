import flask, machine

def get(*args):
	return flask.render_template("bitcoin.html", **(machine.get()))
