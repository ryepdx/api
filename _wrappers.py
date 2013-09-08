import flask

class JsonGet(object):
	def __init__(self, obj):
		self.obj_dict = dict(obj)

	def get(self, request):
		return self.obj_dict

class HtmlGet(JsonGet):
	def get(self, request):
		return flask.render_template(
			"_human.html", 
			_dict = super(HtmlGet, self).get(request)
		)
