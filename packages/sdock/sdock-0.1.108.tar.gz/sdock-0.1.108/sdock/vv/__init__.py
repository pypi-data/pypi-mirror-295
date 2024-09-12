import os,sys
from abc import ABC, abstractmethod

def datetime_valid(dt_str):
	from datetime import datetime
	try:
		datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
	except:
		return False
	return True

class Provider(ABC):
	@abstractmethod
	def install(self):
		pass

	@abstractmethod
	def uninstall(self):
		pass

	@abstractmethod
	def vagrant_string(self, timeoffset=None):
		pass

	@abstractmethod
	def disable_network(self):
		pass

	@abstractmethod
	def disable_timesync(self):
		pass

	@abstractmethod
	def on(self):
		pass

	@abstractmethod
	def off(self):
		pass

	@property
	@abstractmethod
	def raw_name(self):
		pass

	@abstractmethod
	def exe_name(self):
		pass

	def set_exe(self, exe):
		self._exe = exe
	
	def exe(self, string):
		self._exe("{0} {1}".format(self.exe_name(), string))

	def __enter__(self):
		self.on()
		return self

	def __exit__(self, a=None, b=None, c=None):
		self.off()
	
	def inverse(self):
		class stub(object):
			def __init__(self, on_func, off_func):
				self.on_func = on_func
				self.off_func = off_func

			def __enter__(self):
				self.off_func()

			def __exit__(self, a=None, b=None, c=None):
				self.on_func()

		return stub(self.on, self.off)