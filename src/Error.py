# -*- coding: utf-8 -*-

import traceback

__all__ = (
	'Error'
)


class Error(BaseException):
	"""Error Class of Web Application"""

	def __init__(self, reason, status, message, error=None):
		super(Error, self).__init__(reason)
		self.status = status
		self.message = message
		self.error = error
		return

	@property 
	def traceback(self):
		reason = '{}\n'.format(str(self.error) if self.error else str(self))
		if self.error:
			for line in ''.join(traceback.format_tb(self.error.__traceback__)).strip().split('\n'):
				reason += line + '\n'
		else:
			for line in ''.join(traceback.format_tb(self.__traceback__)).strip().split('\n'):
				reason += line + '\n'
		return reason
	
	@property
	def __traceback__(self):
		if self.error:
			return self.error.__traceback__
		return super(Error, self).__traceback__
