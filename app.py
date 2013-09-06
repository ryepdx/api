#!/usr/bin/env python2.6
import flask
import os
import logging

app = flask.Flask(__name__)

# Purposely not a route.
# This is a helper function.
def _get_module(module):
	if os.path.isdir(module):
		return __import__(module, fromlist=[''])
	else:
		flask.abort(404)

@app.route('/hello')
def test():
	return "Hello world."

@app.route('/<module>.html')
def human_readable(module):
	return _get_module(module).human()

@app.route('/<module>.json')
def machine_readable(module):
	return flask.json.jsonify(_get_module(module).machine())
