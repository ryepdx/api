#!/usr/bin/env python2.6
from flup.server.fcgi import WSGIServer
from app import app
WSGIServer(app, debug=True).run()
