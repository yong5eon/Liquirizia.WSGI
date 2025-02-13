# -*- coding: utf-8 -*-
#
# Response Headers
# - ACCEPT_CH: ParseList(),
# - ACCEPT_PATCH: ParseList(fetch=ParseStringWithParameters()),
# - ACCEPT_POST: ParseList(),
# - ACCEPT_RANGES: ParseString(),
# - AGE: ParseInteger(),
# - ALLOW: ParseList(),
# - ALT_SVC: ParseParameters(sep=';'),
# - CLEAR_SITE_DATA: ParseList(),
# - CRITICAL_CH: ParseList(),
# - CROSS_ORIGIN_EMBEDDER_POLICY: ParseString(),
# - CROSS_ORIGIN_OPENER_POLICY: ParseString(),
# - CROSS_ORIGIN_RESOURCE_POLICY: ParseString(),
# - EXPECT_CT: ParseExpectCT(),
# - EXPIRES: ParseDate(),
# - LOCATION: ParseString(),
# - NEL: ParseJSON(),
# - NO_VARY_SEARCH: ParseNoVarySearch(),
# - OBSERVE_BROWSING_TOPICS: ParseBoolean(true='?1'),
# - ORIGIN_AGENT_CLUSTER: ParseBoolean(true='?'),
# - PERMISSIONS_POLICY: ParsePermissionsPolicy(),
# - PROXY_AUTHENTICATE: ParseProxyAuthenticate(),
# - REFERER_POLICY: ParseList(),
# - REFRESH: ParseRefresh(),
# - REPORT_TO: ParseJSON(),
# - REPORTING_ENDPOINTS: ParseParameters(),
# - RETRY_AFTER: ParseRetryAfter(),
# - SERVER: ParseString(),
# - SERVER_TIMING: ParseServerTiming(),
# - SERVICE_WORKER_ALLOWED: ParseString(),
# - SET_COOKIE: # TODO,
# - SET_LOGIN: ParseString(),
# - SOURCEMAP: ParseString(),
# - SPECULATION_RULES: ParseList(),
# - STRICT_TRANSPORT_SECURITY: ParseStrictTransportSecurity(),
# - SUPPORTS_LOADING_MODE: ParseString(),
# - TIMING_ALLOW_ORIGIN: ParseList(),
# - TK: ParseString(),
# - VARY: ParseList(),
# - WWW_AUTHENTICATE: ParseWWWAuthenticate(),
# - X_CONTENT_TYPE_OPTIONS: ParseString(),
# - X_DNS_PREFETCH_CONTROL: ParseBoolean(true='on', false='off'),
# - X_FRAME_OPTIONS: ParseString(),
# - X_PERMITTED_CROSS_DOMAIN_POLICIES: ParseString(),
# - X_POWERED_BY: ParseString(),
# - X_ROBOTS_TAG: ParseXRobotsTag(),
# - X_XSS_PROTECTION: ParseXXSSProtection(), 

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
	ParseJSON,
)

from dataclasses import dataclass
from datetime import datetime
from re import match, findall
from json import loads
from typing import List, Union, Dict

__all__ = (
	'ExpectCT',
	'ParseExpectCT',
	'NoVarySearch',
	'ParseNoVarySearch',
	'PermissionsPolicy',
	'ParsePermissionsPolicy',
	'ProxyAuthenticate',
	'ParseProxyAuthenticate',
	'Refresh',
	'ParseRefresh',
	'ParseRetryAfter',
	'ServerTiming',
	'ParseServerTiming',
	'StrictTransportSecurity',
	'ParseStrictTransportSecurity',
	'WWWAuthenticate',
	'ParseWWWAuthenticate',
	'RobotsTag',
	'ParseXRobotsTag',
	'XSSProtection',
	'ParseXXSSProtection',
)


@dataclass
class ExpectCT(object):
	maxAge: int 
	reportUri: str = None
	enforce: bool = None
class ParseExpectCT(Parse):
	def __call__(self, value: str) -> ExpectCT:
		_ = ParseParameters()(value)
		o = ExpectCT(int(self.strip(_['max-age'])))
		if 'report-uri' in _.keys(): o.reportUri = self.strip(_['report-uri'])
		if 'enforce' in _.keys(): o.enforce = True
		return o


@dataclass
class NoVarySearch(object):
	keyOrder: bool = None
	params: Union[list,bool] = None
	excepts: list = None
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


@dataclass
class PermissionsPolicy(object):
	policy: str
	args: list = None
class ParsePermissionsPolicy(Parse):
	def __call__(self, value: str) -> List[PermissionsPolicy]:
		__ = []
		_ = ParseList()(value)
		for token in _:
			k, v = ParseParameter()(self.strip(token))
			params = ParseList(sep=' ')(self.strip(v, prefix='(', postfix=')'))
			__.append(PermissionsPolicy(policy=k, args=params))
		return __


@dataclass
class ProxyAuthenticate(object):
	scheme: str
	token68: str = None
	parameters: dict = None
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


@dataclass
class Refresh(object):
	time: int
	url: str = None
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


@dataclass
class ServerTiming(object):
	name: str
	duration: float = None
	description: str = None
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


@dataclass
class StrictTransportSecurity(object):
	maxAge: int
	includeSubDomains: bool = None
	preload: bool = None
class ParseStrictTransportSecurity(Parse):
	def __call__(self, value: str) -> StrictTransportSecurity:
		params = ParseParameters(sep=';')(self.strip(value))
		o = StrictTransportSecurity(int(params['max-age']))
		if 'includeSubDomains' in params.keys(): o.includeSubDomains = True
		if 'preload' in params.keys(): o.preload = True
		return o


@dataclass
class WWWAuthenticate(object):
	scheme: str
	token68: str = None
	parameters: dict = None
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


@dataclass
class RobotsTag(object):
	rules: str
	bot: str = None
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


@dataclass
class XSSProtection(object):
	filtering: bool
	parameters: dict = None
class ParseXXSSProtection(Parse):
	def __call__(self, value: str) -> XSSProtection:
		_ = self.strip(value).split(';')
		o = XSSProtection(bool(int(self.strip(_[0]))))
		if len(_) > 1:
			o.parameters = ParseParameters()(_[1])
		return o
