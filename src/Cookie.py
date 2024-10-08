# -*- coding: utf-8 -*-

__all__ = (
	'Cookie'
)


class Cookie(object):
	"""Cookie Class"""

	def __init__(
			self,
			name,
			value,
			expires=None,
			path=None,
			domain=None,
			secure=None,
			http=None,
			version=None,
			max=None,
			comment=None
	):
		self.name = name
		self.value = value
		self.expires = expires
		self.path = path
		self.domain = domain
		self.secure = secure
		self.http = http
		self.version = version
		self.max = max
		self.comment = comment
		return

	def __repr__(self):
		return '{}={}{}{}{}{}{}{}{}{}'.format(
			self.name,
			self.value,
			', domain={}'.format(self.domain) if self.domain else '',
			', path={}'.format(self.path) if self.path else '',
			', expires={}'.format(self.expires) if self.expires else '',
			', max={}'.format(self.max) if self.max else '',
			', version={}'.format(self.version) if self.version else '',
			', secure={}'.format(self.secure) if self.secure else '',
			', http={}'.format(self.http) if self.http else '',
			', comment={}'.format(self.comment) if self.comment else '',
		)
