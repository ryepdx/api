#!/usr/bin/env python2.6
import flask
import os
import logging

app = flask.Flask(__name__)

@app.route('/hello')
def test():
	return "Hello world."

@app.route('/<module>/')
def human_readable(module):
	if os.path.isdir(path):
		return __import__(path, fromlist=['']).human()
	else:
		flask.abort(404)
