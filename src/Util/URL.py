# -*- coding: utf-8 -*-

from urllib.parse import urlparse
from urllib.parse import urlencode

__all__ = (
	'ParseURL',
	'ToQueryString',
)


def ParseURL(url):
	try:
		o = urlparse(url)
		return {
			'protocol': o.scheme,
			'host': o.netloc if o.netloc else o.hostname,
			'port': o.port if o.port else 443 if o.scheme == 'https' else 80,
			'uri': '{}{}'.format(o.path, '?{}'.format(o.query) if o.query else ''),
			'path': o.path,
			'query': o.query,
			'username': o.username,
			'password': o.password,
			'params': o.params,
			'secure': o.scheme == 'https'
		}
	except Exception as e:
		return {}


def ToQueryString(params):
	return urlencode(params)
