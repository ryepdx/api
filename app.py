#!/usr/bin/env python2.6
import flask
import os
import inspect
import logging
import werkzeug.exceptions

app = flask.Flask(__name__)

# Defining a couple constants to
# simplify debugging.
MACHINE = ".machine"
HUMAN = ".human"

# Purposely not routes.
# These are helper functions.
def _get_module(path):
	try:
		return __import__(path, fromlist=[''])
	except ImportError:
		print path
		flask.abort(404)

def _fetch_response(module, request):
	http_method = request.method.lower()

	if not hasattr(module, http_method):
		valid_methods = [func[0].upper()
			for func in inspect.getmembers(
			module, predicate = inspect.isfunction)
		]

		raise werkzeug.exceptions.MethodNotAllowed(
			valid_methods = valid_methods)

	return getattr(module, http_method)(request)

# Purposely routes.
# These are not helper functions. :-)
@app.route('/<path:path>.html')
def human_readable(path):
	return _fetch_response(
		_get_module(path.replace('/', '.') + HUMAN), flask.request)
	

@app.route('/<path:path>.json')
def machine_readable(path):
	return flask.json.jsonify(_fetch_response(
		_get_module(path.replace('/', '.') + MACHINE), flask.request)
	)

@app.route('/<path:path>')
def what_are_you(path):
	return flask.render_template(
		"_what_are_you.html", url = flask.request.url.rstrip('/'))
