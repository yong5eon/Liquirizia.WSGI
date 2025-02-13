# -*- coding: utf-8 -*-
#
# Content Headers
# - CONTENT_DIGEST: ParseParameters()
# - CONTENT_DISPOSISION: ParseStringWithParameters()
# - CONTENT_DPR: ParseInteger()
# - CONTENT_ENCODING: ParseList()
# - CONTENT_LANGUAGE: ParseList()
# - CONTENT_LENGTH: ParseInteger()
# - CONTENT_LOCATION: ParseString()
# - CONTENT_RANGE: ParseContentRange()
# - CONTENT_SECURITY_POLICY: ParseParameters(sep=';', paramsep=' ')
# - CONTENT_SECURITY_POLICY_REPORT_ONLY: ParseParameters(sep=';', paramsep=' ')
# - CONTENT_TYPE: ParseContentType()
# - ETAG: ParseETag()
# - LAST_MODIFIED: ParseDate()
# - REPR_DIGEST: ParseParameters()
# - TRAILER: ParseString()
# - TRANSFER_ENCODING: ParseList()
# - WANT_CONTENT_DIGEST: ParseParameters()
# - WANT_REPR_DIGEST: ParseParameters()

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

__all__ = (
	'ContentRange',
	'ParseContentRange',
	'ContentType'
	'ParseContentType',
	'ETag',
	'ParseETag',
)


@dataclass
class ContentRange(object):
	unit: str = None
	start: int = None
	end: int = None
	size: int = None
class ParseContentRange(Parse):
	def __call__(self, value: str) -> ContentRange:
		o = ContentRange()
		ts = self.strip(value).split(' ', maxsplit=1)
		o.unit = self.strip(ts[0])
		rs = ts[1].strip().split('/')
		o.size = int(self.strip(rs[1])) if self.strip(rs[1]) != '*' else None
		if self.strip(rs[0]) == '*':
			o.start = 0
			o.end = None
		else:
			ss = rs[0].strip().split('-')
			o.start= int(ss[0].strip())
			o.end = int(ss[1].strip())
		return o


@dataclass
class ContentType(object):
	type: str = None
	charset: str = None
	boundary: str = None
class ParseContentType(Parse):
	def __call__(self, value: str) -> ContentType:
		o = ContentType()
		type, params = ParseStringWithParameters()(value)
		o.type = self.strip(type)
		o.charset = self.strip(params['charset']) if 'charset' in params else None
		o.boundary= self.strip(params['boundary']) if 'boundary' in params else None
		return o


@dataclass
class ETag(object):
	weakvalidator: bool = None
	etag: str = None
class ParseETag(Parse):
	def __call__(self, value: str) -> ETag:
		o = ETag()
		if value[:2] == 'W/':
			o.weakvalidator = True
			value = value[2:]
		o.etag = self.strip(value)
		return o
