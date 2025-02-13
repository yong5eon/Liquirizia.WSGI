# -*- coding: utf-8 -*-

from dataclasses import dataclass
from datetime import datetime

__all__ = (
	'Accept',
	'AcceptEncoding',
	'CacheControl',
	'KeepAlive',
	'Link',
	'Priority',
	'Upgrade',
	'Via',
	'Warning',
)

@dataclass
class Accept(object):
	"""Accept Class for Accept Header"""
	type: str = None
	mimetype: str = None
	subtype: str = None
	q: float = None


@dataclass
class AcceptEncoding(object):
	"""Accept Encoding Class for Accept-Encoding Header"""
	compression: str = None
	q: float = 1.0


@dataclass
class CacheControl(object):
	"""Cache Control Class for Cache-Control Header"""
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
	

@dataclass
class KeepAlive(object):
	"""Keep Alive Class for Keep-Alive Header"""
	timeout: int = None
	max: int = None
	

@dataclass
class Link(object):
	"""Link Class for Link Header"""
	url: str = None
	rel: str = None
	parameters: dict = None


@dataclass
class Priority(object):
	"""Priority Class for PriorityClass"""
	urgency: int = None
	incremental: bool = None


@dataclass
class Upgrade(object):
	"""Upgrade Class for Upgrade Header"""
	protocolstr: str = None
	protocol: str = None
	version: str = None


@dataclass
class Via(object):
	"""Via Class for Via Header"""
	protocol: str = None
	version: str = None
	host: str = None
	port: int = None


@dataclass
class Warning(object):
	"""Warning Class for Warning Header"""
	code: str = None
	agent: str = None
	text: str = None
	date: datetime = None
