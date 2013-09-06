#!/usr/bin/env python2.6
import flask
import os
import logging

app = flask.Flask(__name__)

# Purposely not a route.
# This is a helper function.
def _get_module(module):
	if os.path.isdir(path):
		return __import__(path, fromlist=['']).human()
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
	return _get_module(module).machine()
