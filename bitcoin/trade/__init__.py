from models import Order
from types import ModuleType
import sys
import get, post

def __getattr__(attr):
	order = Order.query.filter_by(token = attr).first()
	if order != None:
		return order
	raise AttributeError
