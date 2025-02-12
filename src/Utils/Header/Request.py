# -*- coding: utf-8 -*-
#
# Request Headers
# - ACCEPT_LANGUAGE: ParseAcceptLanguage()
# - ALT_USED: ParseAltUsed()
# - AUTHORIZATION: ParseAuthorization()
# - COOKIE: ParseCookie()
# - DEVICE_MEMORY: ParseFloat()
# - DNT: ParseInteger()
# - DOWNLINK: ParseFloat()
# - DPR: ParseFloat()
# - EARLY_DATA: ParseInteger()
# - ECT: ParseString()
# - EXPECT: ParseString()
# - FORWARDED: ParseParameters()
# - FROM: ParseString()
# - HOST: ParseString()
# - IF_MATCH: ParseList()
# - IF_MODIFIED_SINCE: ParseDate()
# - IF_NONE_MATCH: ParseList()
# - IF_RANGE: ParseIfRange()
# - IF_UNMODIFIED_SINCE: ParseDate()
# - MAX_FORWARDS: ParseInteger()
# - ORIGIN: ParseString()
# - PROXY_AUTHORIZATION: ParseProxyAuthorization()
# - RANGE: ParseRange()
# - REFERER: ParseString()
# - RTT: ParseFloat()
# - SAVE_DATA: ParseString()
# - SEC_BROWSING_TOPICS: ParseString()
# - SEC_CH_PREFERS_COLOR_SCHEME: ParseString()
# - SEC_CH_PREFERS_REDUCED_MOTION: ParseString()
# - SEC_CH_PREFERS_REDUCED_TRANSPARENCY: ParseString()
# - SEC_CH_UA: ParseList()
# - SEC_CH_UA_ARCH: ParseString()
# - SEC_CH_UA_BITNESS: ParseInteger()
# - SEC_CH_UA_FULL_VERSION: ParseString()
# - SEC_CH_UA_FULL_VERSION_LIST: ParseList()
# - SEC_CH_UA_MOBILE: ParseBoolean(true='?1', false='?0')
# - SEC_CH_UA_MODEL: ParseString()
# - SEC_CH_UA_PLATFORM: ParseString()
# - SEC_CH_UA_PLATFORM_VERSION: ParseString()
# - SEC_FETCH_DEST: ParseString()
# - SEC_FETCH_MODE: ParseString()
# - SEC_FETCH_SITE: ParseString()
# - SEC_FETCH_USER: ParseString()
# - SEC_GPC: ParseBoolean(true='1', false='0')
# - SEC_PURPOSE: ParseString()
# - SERVICE_WORKER: ParseString()
# - SERVICE_WORKER_NAVIGATION_PRELAOD: ParseString()
# - TE: ParseTE()
# - UPGRADE_INSECURE_REQUESTS: ParseBoolean(true='1')
# - USER_AGENT: ParseString()
# - VIEWPORT_WIDTH: ParseInteger()
# - WIDTH: ParseInteger()
# - X_FORWARDED_FOR: ParseList()
# - X_FORWARDED_HOST: ParseString()
# - X_FORWARDED_PROTO: ParseString()

from ..Parse import (
	Parse,
	ParseBoolean,
	ParseString,
	ParseStringWithParameters,
	ParseInteger,
	ParseFloat,
	ParseDate,
	ParseParameter,
	ParseParameters,
	ParseList,
)

from dataclasses import dataclass
from datetime import datetime
from http.cookies import SimpleCookie
from re import findall
from typing import List, Tuple, Union

__all__ = (
	'AcceptLanguage',
	'ParseAcceptLanguage',
	'AltUsed',
	'ParseAltUsed',
	'Authorization',
	'ParseAuthorization',
	'Cookie',
	'ParseCookie',
	'ParseIfRange',
	'ProxyAuthorization',
	'ParseProxyAuthorization',
	'Range',
	'ParseRange',
	'SecCHUA',
	'ParseSecCHUA',
	'SecCHUAFullVersion',
	'ParseSecCHUAFullVersion',
	'TE',
	'ParseTE',
)


@dataclass
class AcceptLanguage(object):
	language: str = None
	q: float = 1.0
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

@dataclass
class AltUsed(object):
	host: str = None
	port: int = None
class ParseAltUsed(Parse):
	def __call__(self, value: str) -> AltUsed:
		_ = AltUsed()
		ts = self.strip(value).split(':', maxsplit=1)
		_.host = self.strip(ts[0])
		_.port = int(self.strip(ts[1])) if len(ts) > 1 else None
		return _

@dataclass
class Authorization(object):
	scheme: str = None
	credentials: str = None
	parameters: dict = None
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


@dataclass
class Cookie(object):
	name = None
	value = None
	expires = None
	path = None
	domain = None
	secure = None
	http = None
	version = None
	maxage = None
	comment = None
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


@dataclass
class ProxyAuthorization(object):
	scheme: str = None
	credentials: str = None
class ParseProxyAuthorization(Parse):
	def __call__(self, value: str) -> ProxyAuthorization:
		_ = ProxyAuthorization()
		ts = self.strip(value).split(' ', maxsplit=1)
		_.scheme = self.strip(ts[0])
		_.credentials = self.strip(ts[1])
		return _


@dataclass
class Range(object):
	start: int = None
	end: int = None
	suffixLength: int = None
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
	

@dataclass
class SecCHUA(object):
	brand: str = None
	significantVersion: str = None
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


@dataclass
class SecCHUAFullVersion(object):
	brand: str = None
	fullVersion: str = None
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


@dataclass
class TE(object):
	transferCoding: str = None
	q: float = 1.0
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
