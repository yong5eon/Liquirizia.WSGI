# -*- coding: utf-8 -*-

from .Common import (
	Accept,
	AcceptEncoding,
	CacheControl,
	KeepAlive,
	Link,
	Priority,
	Upgrade,
	Via,
	Warning,
)
from .Content import (
	ContentRange,
	ContentType,
	ETag,
)
from .Request import (
	AcceptLanguage,
	AltUsed,
	Authorization,
	Cookie,
	ProxyAuthorization,
	Range,
	SecCHUA,
	SecCHUAFullVersion,
	TE,
	UserAgent,
)
from .Response import (
	ExpectCT,
	NoVarySearch,
	PermissionsPolicy,
	ProxyAuthenticate,
	Refresh,
	ServerTiming,
	StrictTransportSecurity,
	WWWAuthenticate,
	RobotsTag,
	XSSProtection,
)

__all__ = (
	# Common Headers
	'Accept',
	'AcceptEncoding',
	'CacheControl',
	'KeepAlive',
	'Link',
	'Priority',
	'Upgrade',
	'Via',
	'Warning',
	# Content Headers
	'ContentRange',
	'ContentType',
	'ETag',
	# Request Headers
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
	# Reponse Headers
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
