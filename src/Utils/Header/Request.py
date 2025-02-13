# -*- coding: utf-8 -*-

from .Parse import (
	Parse,
	ParseStringWithParameters,
	ParseList,
)
from ...Headers import *

from datetime import datetime
from http.cookies import SimpleCookie
from re import findall
from typing import List, Tuple, Union

__all__ = (
	'ParseAcceptLanguage',
	'ParseAltUsed',
	'ParseAuthorization',
	'ParseCookie',
	'ParseIfRange',
	'ParseProxyAuthorization',
	'ParseRange',
	'ParseSecCHUA',
	'ParseSecCHUAFullVersion',
	'ParseTE',
)


class ParseAcceptLanguage(Parse):
	def __call__(self, value: str) -> List[AcceptLanguage]:
		_ = []
		als = ParseList()(value)
		for al in als:
			lang, params = ParseStringWithParameters()(al)
			o = AcceptLanguage()
			o.language = self.strip(lang)
			if 'q' in params.keys(): o.q = float(params['q'])
			_.append(o)
		_ = sorted(_, key=lambda x: x.q, reverse=True)
		return _


class ParseAltUsed(Parse):
	def __call__(self, value: str) -> AltUsed:
		_ = AltUsed()
		ts = self.strip(value).split(':', maxsplit=1)
		_.host = self.strip(ts[0])
		_.port = int(self.strip(ts[1])) if len(ts) > 1 else None
		return _


class ParseAuthorization(Parse):
	def __call__(self, value: str) -> Authorization:
		_ = Authorization()
		ts = self.strip(value).split(' ', maxsplit=1)
		if ts[0].strip().lower() == 'digest':
			_.scheme = self.strip(ts[0])
			_.credentials = None
			_.parameters = {}
			for token in self.strip(ts[1]).split(','):
				k, v = self.strip(token).split('=')
				_.parameters[self.strip(k)] = self.strip(v)
		else:
			_.scheme = self.strip(ts[0])
			_.credentials = self.strip(ts[1])
			_.parameters = {}
		return _


class ParseCookie(Parse):
	def __call__(self, value: str) -> List[Cookie]:
		_ = []
		c = SimpleCookie()
		c.load(value)
		for k, v in c.items():
			o = Cookie()
			o.name=k
			o.value=v.value
			o.expires=v['expires']
			o.path=v['path']
			o.domain=v['domain']
			o.secure=v['secure']
			o.http=v['httponly']
			o.version=v['version']
			o.maxage=v['max-age']
			o.comment=v['comment']
			_.append(o)
		return _


class ParseIfRange(Parse):
	def __call__(self, value: str) -> Union[datetime, str]:
		try:
			return datetime.strptime(self.strip(value), '%a, %d %b %Y %H:%M:%S GMT')
		except:
			return self.strip(value)


class ParseProxyAuthorization(Parse):
	def __call__(self, value: str) -> ProxyAuthorization:
		_ = ProxyAuthorization()
		ts = self.strip(value).split(' ', maxsplit=1)
		_.scheme = self.strip(ts[0])
		_.credentials = self.strip(ts[1])
		return _


class ParseRange(Parse):
	def __call__(self, value: str) -> Tuple[str, List[Range]]:
		unit, ranges = self.strip(value).split('=', maxsplit=1)
		__ = []
		_ = ParseList()(ranges)
		for token in _:
			__.append(self.__parse__(self.strip(token)))
		return unit, __
	def __parse__(self, range: str) -> Range:
		_ = Range()
		offset, end = range.split('-')
		if not offset:	# bytes=-100 : last 100 bytes
			_.suffixLength = int(self.strip(end))
		elif not end:	# bytes=100- : all but the first 99 bytes
			_.start = int(self.strip(offset))
		else:	# bytes=100-200 : bytes 100-200 (inclusive)
			_.start = int(self.strip(offset))
			_.end = int(self.strip(end))
		return _
	

class ParseSecCHUA(Parse):
	def __call__(self, value: str) -> List[SecCHUA]:
		_ = []
		pattern = r'"([^"]+)";v="([^"]+)"'
		matches = findall(pattern, value)
		for brand, version in matches:
			o = SecCHUA()
			o.brand = self.strip(brand)
			o.significantVersion = self.strip(version)
			_.append(o)
		return _


class ParseSecCHUAFullVersion(Parse):
	def __call__(self, value: str) -> List[SecCHUAFullVersion]:
		_ = []
		pattern = r'"([^"]+)";v="([^"]+)"'
		matches = findall(pattern, value)
		for brand, version in matches:
			o = SecCHUAFullVersion()
			o.brand = self.strip(brand)
			o.fullVersion = self.strip(version)
			_.append(o)
		return _


class ParseTE(Parse):
	def __call__(self, value: str) -> List[TE]:
		__ = []
		_ = ParseList()(value)
		for token in _:
			v, params = ParseStringWithParameters()(token)
			o = TE()
			o.transferCoding = v
			if 'q' in params.keys(): o.q = float(params['q'])
			__.append(o)
		__ = sorted(__, key=lambda x: x.q, reverse=True)
		return __
