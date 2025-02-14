# -*- coding: utf-8 -*-

from dataclasses import dataclass

__all__ = (
	'AcceptLanguage',
	'AltUsed',
	'Authorization',
	'Cookie',
	'ProxyAuthorization',
	'Range',
	'SecCHUA',
	'SecCHUAFullVersion',
	'TE',
	'UserAgent',
)


@dataclass
class AcceptLanguage(object):
	"""Accept Language Class for Accept-Language Header"""
	language: str = None
	q: float = 1.0


@dataclass
class AltUsed(object):
	"""Alt Used Class for Alt-Used Header"""
	host: str = None
	port: int = None


@dataclass
class Authorization(object):
	"""Authorization Class for Authroziation Header"""
	scheme: str = None
	credentials: str = None
	parameters: dict = None


@dataclass
class Cookie(object):
	"""Cookie Class for Cookie Header"""
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


@dataclass
class ProxyAuthorization(object):
	"""Proxy Authorization Class for Proxy-Authorization Header"""
	scheme: str = None
	credentials: str = None


@dataclass
class Range(object):
	"""Range Class for Range Header"""
	start: int = None
	end: int = None
	suffixLength: int = None


@dataclass
class SecCHUA(object):
	"""SecCHUA Class for Sec-CH-UA Header"""
	brand: str = None
	significantVersion: str = None


@dataclass
class SecCHUAFullVersion(object):
	"""SecCHUAFullVersion Class for Sec-CH-UA-Full-Version Header"""
	brand: str = None
	fullVersion: str = None


@dataclass
class TE(object):
	"""TE(Transfer Encoding) Class for TE Header"""
	transferCoding: str = None
	q: float = 1.0


@dataclass
class UserAgent(object):
	product: str
	version: str
	comment: str
	system: str = None
	platform: str = None
	platformDetails: str = None
	extensions: list = None
