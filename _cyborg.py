import sys
import os

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
	                        cyborg = self.module.__getattr__(attr_root)
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
