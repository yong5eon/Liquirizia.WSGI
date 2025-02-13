# -*- coding: utf-8 -*-
#
# Common Headers
# - ACCEPT : ParseAccept()
# - ACCEPT_ENCODING : ParseAcceptEncoding()
# - CACHE_CONTROL : ParseCacheControl()
# - CONNECTION : ParseString()
# - DATE : ParseDate()
# - KEEP_ALIVE : ParseParameters()
# - LINK : ParseLink()
# - PRAGMA : ParseString()
# - PRIORITY : ParsePriority()
# - UPGRADE : ParseUpgrade()
# - VIA : ParseVia()
# - WARNING : ParseString()

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
from re import split
from typing import List

__all__ = (
	'Accept',
	'ParseAccept',
	'AcceptEncoding',
	'ParseAcceptEncoding',
	'CacheControl',
	'ParseCacheControl',
	'KeepAlive',
	'ParseKeepAlive',
	'Link',
	'ParseLink',
	'Priority',
	'ParsePriority',
	'Upgrade',
	'ParseUpgrade',
	'Via',
	'ParseVia',
	'Warning',
	'ParseWarning',
)

@dataclass
class Accept(object):
	type: str = None
	mimetype: str = None
	subtype: str = None
	q: float = None
class ParseAccept(Parse):
	def __call__(self, value: str) -> List[Accept]:
		__ = []
		_ = ParseList()(value)
		for token in _:
			v, params = ParseStringWithParameters()(token)
			o = Accept()
			o.type = v
			o.mimetype, o.subtype = v.split('/')
			if 'q' not in params.keys(): o.q = 1.0
			else: o.q = float(params['q'])
			__.append(o)
		__ = sorted(__, key=lambda x: x.q, reverse=True)
		return __


@dataclass
class AcceptEncoding(object):
	compression: str = None
	q: float = 1.0
class ParseAcceptEncoding(Parse):
	def __call__(self, value: str) -> List[AcceptEncoding]:
		__ = []
		_ = ParseList()(value)
		for token in _:
			v, params = ParseStringWithParameters()(token)
			o = AcceptEncoding()
			o.compression = v
			if 'q' in params.keys(): o.q = float(params['q'])
			__.append(o)
		__ = sorted(__, key=lambda x: x.q, reverse=True)
		return __


@dataclass
class CacheControl(object):
	noCache: bool = None
	noStore: bool = None
	maxAge: int = None
	maxStable: int = None
	minFresh: int = None
	noTransform: bool = None
	onlyIfCached: bool = None
	shareMaxAge: int = None
	mustRevalidate: bool = None
	proxyRevalidate: bool = None
	private: bool = None
	public: bool = None
	mustUnderstand: bool = None
	immutable: bool = None
	stableWhileRevalidate: int = None
	stableIfError: int = None
class ParseCacheControl(Parse):
	def __call__(self, value: str) -> CacheControl:
		_ = ParseParameters()(value)
		o = CacheControl()
		if 'no-cache' in _.keys(): o.noCache = True
		if 'no-store' in _.keys(): o.noStore = True
		if 'max-age' in _.keys(): o.maxAge = int(self.strip(_['max-age']))
		if 'max-stable' in _.keys(): o.maxStable = int(self.strip(_['max-stable']))
		if 'min-fresh' in _.keys(): o.minFresh = int(self.strip(_['max-fresh']))
		if 'no-transform' in _.keys(): o.noTransform = True
		if 'only-if-cached' in _.keys(): o.onlyIfCached = True
		if 's-maxage' in _.keys(): o.shareMaxAge = int(self.strip(_['s-maxage']))
		if 'must-revalidate' in _.keys(): o.mustRevalidate = True
		if 'proxy-revalidate' in _.keys(): o.proxyRevalidate = True
		if 'private' in _.keys(): o.private = True
		if 'public' in _.keys(): o.public = True
		if 'must-understand' in _.keys(): o.mustUnderstand = True
		if 'immutable' in _.keys(): o.immutable = True
		if 'stable-while-revalidate' in _.keys(): o.stableWhileRevalidate = int(self.strip(_['stable-while-revalidate']))
		if 'stable-if-error' in _.keys(): o.stableIfError = int(self.strip(_['stable-if-error']))
		return o
	

@dataclass
class KeepAlive(object):
	timeout: int = None
	max: int = None
class ParseKeepAlive(Parse):
	def __call__(self, value: str) -> KeepAlive:
		_ = ParseParameters()(value)
		o = KeepAlive()
		if 'timeout' in _.keys(): o.timeout = _['timeout']
		if 'max' in _.keys(): o.max = _['max']
		return o
	

@dataclass
class Link(object):
	url: str = None
	rel: str = None
	parameters: dict = None
class ParseLink(Parse):
	def __call__(self, value: str) -> List[Link]:
		__ = []
		_ = ParseList(fetch=ParseStringWithParameters(sep=';', paramsep=';'))(value)
		for v, params in _:
			o = Link()
			o.url = self.strip(v).replace('<','').replace('>','')
			o.rel = self.strip(params['rel']) if 'rel' in params.keys() else None
			o.parameters = params
			__.append(o)
		return __


@dataclass
class Priority(object):
	urgency: int = None
	incremental: bool = None
class ParsePriority(Parse):
	def __call__(self, value: str) -> Priority:
		_ = ParseParameters()(value)
		o = Priority()
		if 'u' in _.keys(): o.urgency = int(eval(self.strip(_['u'])))
		if 'i' in _.keys(): o.incremental = True
		return o


@dataclass
class Upgrade(object):
	protocolstr: str = None
	protocol: str = None
	version: str = None
class ParseUpgrade(Parse):
	def __call__(self, value: str) -> List[Upgrade]:
		__ = []
		_ = ParseList()(value)
		for token in _:
			ts = self.strip(token).split('/')
			o = Upgrade()
			o.protocolstr = self.strip(token)
			o.protocol = self.strip(ts[0])
			o.version = self.strip(ts[1]) if len(ts) > 1 else None
			__.append(o)
		return __


@dataclass
class Via(object):
	protocol: str = None
	version: str = None
	host: str = None
	port: int = None
class ParseVia(Parse):
	def __call__(self, value) -> List[Via]:
		__ = []
		_ = ParseList()(value)
		for token in _:
			ts = self.strip(token).split(' ')
			o = Via()
			o.version = self.strip(ts[0])
			o.protocol = None
			ptvs = o.version.split('/')
			if len(ptvs) > 1:
				o.protocol = self.strip(ptvs[0])
				o.version = self.strip(ptvs[1])
			o.host = self.strip(ts[1])
			o.port = None
			addrs = o.host.split(':')
			if len(addrs) > 1:
				o.host = self.strip(addrs[0])
				o.port = int(self.strip(addrs[1]))
			__.append(o)
		return __


@dataclass
class Warning(object):
	code: str = None
	agent: str = None
	text: str = None
	date: datetime = None
class ParseWarning(Parse):
	def __call__(self, value: str) -> Warning:
		tokens = split(r' (?=(?:[^"]*"[^"]*")*[^"]*$)', value)
		if len(tokens) < 3:
			raise ValueError("Invalid warning header format")
		o = Warning()
		o.code = self.strip(tokens[0])
		o.agent = self.strip(tokens[1])
		o.text = self.strip(tokens[2])
		if len(tokens) == 4: o.date = self.strip(tokens[3])
		return o
