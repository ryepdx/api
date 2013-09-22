from models import Order
from types import ModuleType
import sys

def __getattr__(attr):
	order = Order.query.filter_by(token = attr).first()
	if order != None:
		return order
	raise AttributeError
