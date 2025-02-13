# -*- coding: utf-8 -*-

from dataclasses import dataclass

__all__ = (
	'ContentRange',
	'ContentType'
	'ETag',
)


@dataclass
class ContentRange(object):
	"""Content Range Class for Content-Range Header"""
	unit: str = None
	start: int = None
	end: int = None
	size: int = None


@dataclass
class ContentType(object):
	"""Content Type Class for Content-Type Header"""
	type: str = None
	charset: str = None
	boundary: str = None


@dataclass
class ETag(object):
	"""ETag Class for ETag Header"""
	weakvalidator: bool = None
	etag: str = None
