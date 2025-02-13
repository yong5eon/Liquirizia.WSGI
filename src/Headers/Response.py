# -*- coding: utf-8 -*-

from dataclasses import dataclass
from datetime import datetime
from re import match, findall
from json import loads
from typing import List, Union, Dict

__all__ = (
	'ExpectCT',
	'NoVarySearch',
	'PermissionsPolicy',
	'ProxyAuthenticate',
	'Refresh',
	'ServerTiming',
	'StrictTransportSecurity',
	'WWWAuthenticate',
	'RobotsTag',
	'XSSProtection',
)


@dataclass
class ExpectCT(object):
	"""Expect CT Class for Expect-CT Header"""
	maxAge: int 
	reportUri: str = None
	enforce: bool = None


@dataclass
class NoVarySearch(object):
	"""No Vary Search Class for No-Vary-Search Header"""
	keyOrder: bool = None
	params: Union[list,bool] = None
	excepts: list = None


@dataclass
class PermissionsPolicy(object):
	"""Permissions Policy Class for Permissions-Policy Header"""
	policy: str
	args: list = None


@dataclass
class ProxyAuthenticate(object):
	"""Proxy Authenticate Class for Proxy-Authenticate Header"""
	scheme: str
	token68: str = None
	parameters: dict = None


@dataclass
class Refresh(object):
	"""Refresh Class for Refresh Header"""
	time: int
	url: str = None


@dataclass
class ServerTiming(object):
	"""Server Timing Class for Server-Timing Header"""
	name: str
	duration: float = None
	description: str = None


@dataclass
class StrictTransportSecurity(object):
	"""Strict Transport Security Class for Strict-Transfort-Security Header"""
	maxAge: int
	includeSubDomains: bool = None
	preload: bool = None


@dataclass
class WWWAuthenticate(object):
	"""WWW Authenticate Class for WWW-Authenticate Header"""
	scheme: str
	token68: str = None
	parameters: dict = None


@dataclass
class RobotsTag(object):
	"""Robots Tag Class for X-Robots-Tag Header"""
	rules: str
	bot: str = None


@dataclass
class XSSProtection(object):
	"""XSS Protection Class for X-XSS-Protection Header"""
	filtering: bool
	parameters: dict = None
