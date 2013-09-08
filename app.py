#!/usr/bin/env python2.6
import flask
import os
import sys
import inspect
import logging
import settings
import werkzeug.exceptions
from flask.ext.sqlalchemy import SQLAlchemy
from _cyborg import Cyborg

app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = settings.DB_URI
db = SQLAlchemy(app)
queen_borg = Cyborg(sys.modules[__name__])

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
@app.route('/<path:path>.html', methods=["POST","GET"])
def human_readable(path):
	print path
	return _fetch_response(
		getattr(queen_borg, path.replace('/', '.')).human, flask.request)
	

@app.route('/<path:path>.json', methods=["POST", "GET"])
def machine_readable(path):
	return flask.json.jsonify(_fetch_response(
		getattr(queen_borg, path.replace('/', '.')).machine, flask.request)
	)

@app.route('/<path:path>')
def what_are_you(path):
	return flask.render_template(
		"_what_are_you.html", url = flask.request.url.rstrip('/'))
