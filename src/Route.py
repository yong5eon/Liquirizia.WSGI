# -*- coding: utf-8 -*-

from re import compile, escape

__all__ = (
	'Route'
)


class Route(object):
	RegexVar = compile(r':\w+')

	def __init__(self, method: str, url: str, parameter: str = ':%s'):
		self.method = method
		self.url = url
		self.parameter = parameter
		self.re, self.fmt = self.parse(url)
		return

	def match(self, url: str):
		m = self.re.match(url)
		if not m:
			return False, None
		return True, m.groupdict()

	def parse(self, url: str):
		fmt = []
		regex = []
		pos = 0

		for match in Route.RegexVar.finditer(url):
			regex.append(escape(url[pos:match.start()]))
			fmt.append(url[pos:match.start()])

			regex.append('(?P<%s>%s)' % (match.group()[1:], '[^/]+'))
			fmt.append(self.parameter % (match.group()[1:],))

			pos = match.end()

		regex.append(escape(url[pos:]))
		fmt.append(url[pos:])

		return compile('^%s$' % "".join(regex)), "".join(fmt)
