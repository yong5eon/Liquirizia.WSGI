# -*- coding: utf-8 -*-

from .URL import (
	ParseURL,
	ToQueryString,
)
from .Header import (
	ToHeaderName,
	ParseHeader,
	ParseRange,
)

from email.utils import parsedate_tz
from time import timezone, mktime

__all__ = (
	'ToHeaderName',
	'ToQueryString',
	'ParseHeader',
	'ParseRange',
	'ParseURL',
	'VersionToString',
	'DateToTimestamp',
	'HeadersToMap',
)


def VersionToString(version):
	return {
		10: 'HTTP/1.0',
		11: 'HTTP/1.1',
		20: 'HTTP/2.0',
	}.get(version, 10)


def DateToTimestamp(str):
	""" Parse rfc1123, rfc850 and asctime timestamps and return UTC epoch. """
	try:
		ts = parsedate_tz(str)
		return mktime(ts[:8] + (0,)) - (ts[9] or 0) - timezone
	except (TypeError, ValueError, IndexError, OverflowError):
		return None
