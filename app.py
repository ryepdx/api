#!/usr/bin/env python2.6
import flask
import os
import sys
import settings
import werkzeug.exceptions
from flask.ext.sqlalchemy import SQLAlchemy
from cyborg import Cyborg

app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = settings.DB_URI
db = SQLAlchemy(app)

@app.route('/bitcoin/order<extension>', methods=["POST", "GET"])
def redir(extension):
	return flask.redirect("/bitcoin/trade%s" % extension)

# Wrap this module in a Cyborg instance,
# and then setup the default Cyborg routes.
(Cyborg(sys.modules[__name__])).setup(app, human_ext=".html")

@app.route('/<path:path>')
def what_are_you(path):
	return flask.render_template(
		"_what_are_you.html", url = flask.request.url.rstrip('/'))
