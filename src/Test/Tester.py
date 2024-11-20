# -*- coding: utf-8 -*-

from ..Application import Application

from typing import Dict

__all__ = (
)


class Sender(object):
	def __init__(self):
		pass

	def __call__(self, *args, **kwds):
		pass


class Tester(object):
	def __init__(
		self,
		application: Application,
		env: Dict = None,
	):
		self.application = application
		self.envs = env
		return
	
	def send(self):
		pass

	def write(self):
		pass
	
	def get(self, uri: str, qs: Dict = None, headers: Dict = None):
		env = {}
		sender = Sender()
		self.application(env, send=Sender())
		return sender.response