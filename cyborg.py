import sys
import os
import inspect
import logging
import flask

class Cyborg(object):
	def __init__(self, module, import_path=[]):
		self.module = module
		self.import_path = import_path

	def __getattr__(self, attr):
		attrs = attr.split('.')
		attr_root = attrs.pop(0)
		module_path = os.path.dirname(self.module.__file__)

		try:
			if hasattr(self.module, "__getattr__"):
				try:
					cyborg = self.module.__getattr__(attr_root)
				except AttributeError:
					cyborg = getattr(self.module, attr_root)
			else:
				cyborg = getattr(self.module, attr_root)
		except AttributeError:
			if not (os.path.exists(module_path + '/' + attr_root + ".py")
			or os.path.exists(module_path + '/' + attr_root + "/__init__.py")):
				raise
			import_path = self.import_path + [attr_root]
			__import__('.'.join(import_path))

			cyborg = Cyborg(sys.modules['.'.join(import_path)
				], import_path = import_path)
				
		if attrs:
			return cyborg.__getattr__('.'.join(attrs))
		return cyborg

	# Internal helper function.
	def _fetch_response(self, module, request):
		http_method = request.method.lower()

		if not hasattr(module, http_method):
			valid_methods = [func[0].upper()
				for func in inspect.getmembers(
				module, predicate = inspect.isfunction)
			]

			raise werkzeug.exceptions.MethodNotAllowed(
				valid_methods = valid_methods)

		return getattr(module, http_method)(request)

	# Sets up the default Cyborg routes.
	# Should only ever get called on the root Cyborg object.
	def setup(self, app, human_ext='', machine_ext='.json'):

		# Cyborg foundational routes.
		@app.route('/<path:path>%s' % human_ext, methods=["POST","GET"])
		def human_readable(path):
			return self._fetch_response(
				getattr(self, path.replace('/', '.')).human, flask.request)
	
		@app.route('/<path:path>%s' % machine_ext, methods=["POST", "GET"])
		def machine_readable(path):
			return flask.json.jsonify(self._fetch_response(
				getattr(self, path.replace('/', '.')).machine, flask.request)
			)
