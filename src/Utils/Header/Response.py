# -*- coding: utf-8 -*-

from .Parse import (
	Parse,
	ParseParameter,
	ParseParameters,
	ParseList,
)
from ...Headers import *

from datetime import datetime
from re import match
from typing import List, Union

__all__ = (
	'ParseExpectCT',
	'ParseNoVarySearch',
	'ParsePermissionsPolicy',
	'ParseProxyAuthenticate',
	'ParseRefresh',
	'ParseRetryAfter',
	'ParseServerTiming',
	'ParseStrictTransportSecurity',
	'ParseWWWAuthenticate',
	'ParseXRobotsTag',
	'ParseXXSSProtection',
)


class ParseExpectCT(Parse):
	def __call__(self, value: str) -> ExpectCT:
		_ = ParseParameters()(value)
		o = ExpectCT(int(self.strip(_['max-age'])))
		if 'report-uri' in _.keys(): o.reportUri = self.strip(_['report-uri'])
		if 'enforce' in _.keys(): o.enforce = True
		return o


class ParseNoVarySearch(Parse):
	def __call__(self, value: str) -> NoVarySearch:
		_ = ParseParameters()(value)
		o = NoVarySearch()
		if 'key-order' in _.keys(): o.keyOrder = True
		if 'params' in _.keys():
			if _['params']: 
				o.params = ParseList(sep=' ')(self.strip(_['params'], prefix='(', postfix=')'))
			else:
				o.params = True
		if 'except' in _.keys():
			o.excepts = ParseList(sep=' ')(self.strip(_['except'], prefix='(', postfix=')'))
		return o


class ParsePermissionsPolicy(Parse):
	def __call__(self, value: str) -> List[PermissionsPolicy]:
		__ = []
		_ = ParseList()(value)
		for token in _:
			k, v = ParseParameter()(self.strip(token))
			params = ParseList(sep=' ')(self.strip(v, prefix='(', postfix=')'))
			__.append(PermissionsPolicy(policy=k, args=params))
		return __


class ParseProxyAuthenticate(Parse):
	def __call__(self, value: str) -> ProxyAuthenticate:
		scheme, args = self.strip(value).split(' ', maxsplit=1)
		_ = ProxyAuthenticate(self.strip(scheme))
		tokens = self.strip(args).split(',')
		if len(tokens) > 1:
			_.parameters = ParseParameters()(args)
		else:
			_.token68 = self.strip(tokens[0])
		return _


class ParseRefresh(Parse):
	def __call__(self, value: str) -> Refresh:
		m = match(r'(\d+)\s*[;,]?\s*url=(.*)', value)
		if m:
			time = int(self.strip(m.group(1)))
			url = self.strip(m.group(2)) if m.group(2) else None
		else:
			time = int(self.strip(value))
			url = None
		return Refresh(time=time, url=url)


class ParseRetryAfter(Parse):
	def __call__(self, value: str) -> Union[datetime, str]:
		try:
			return datetime.strptime(self.strip(value), '%a, %d %b %Y %H:%M:%S GMT')
		except:
			return int(self.strip(value))


class ParseServerTiming(Parse):
	def __call__(self, value: str) -> List[ServerTiming]:
		__ = []
		tokens = ParseList()(self.strip(value))
		for token in tokens:
			_ = self.strip(token).split(';', maxsplit=1)
			o = ServerTiming(self.strip(_[0]))
			if len(_) > 1:
				params = ParseParameters(sep=';')(_[1])
				if 'dur' in params.keys(): o.duration = float(self.strip(params['dur']))
				if 'desc' in params.keys(): o.description = self.strip(params['desc'])
			__.append(o)
		return __


class ParseStrictTransportSecurity(Parse):
	def __call__(self, value: str) -> StrictTransportSecurity:
		params = ParseParameters(sep=';')(self.strip(value))
		o = StrictTransportSecurity(int(params['max-age']))
		if 'includeSubDomains' in params.keys(): o.includeSubDomains = True
		if 'preload' in params.keys(): o.preload = True
		return o


class ParseWWWAuthenticate(Parse):
	def __call__(self, value: str) -> WWWAuthenticate:
		scheme, args = self.strip(value).split(' ', maxsplit=1)
		_ = WWWAuthenticate(self.strip(scheme))
		tokens = self.strip(args).split(',')
		if len(tokens) > 1:
			_.parameters = ParseParameters()(args)
		else:
			_.token68 = self.strip(tokens[0])
		return _


class ParseXRobotsTag(Parse):
	def __call__(self, value: str) -> RobotsTag:
		tokens = self.strip(value).split(':', maxsplit=1)
		rules = []
		bot = None
		if len(tokens) > 1:
			rulestr = self.strip(tokens[1])
			bot = self.strip(tokens[0])
		else:
			rulestr = self.strip(tokens[0])
		rules = ParseList()(rulestr)
		return RobotsTag(rules=rules, bot=bot)


class ParseXXSSProtection(Parse):
	def __call__(self, value: str) -> XSSProtection:
		_ = self.strip(value).split(';')
		o = XSSProtection(bool(int(self.strip(_[0]))))
		if len(_) > 1:
			o.parameters = ParseParameters()(_[1])
		return o
