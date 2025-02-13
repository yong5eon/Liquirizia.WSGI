# -*- coding: utf-8 -*-

from .Parse import (
	Parse,
	ParseStringWithParameters,
)

from ...Headers import *

__all__ = (
	'ParseContentRange',
	'ParseContentType',
	'ParseETag',
)


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


class ParseContentType(Parse):
	def __call__(self, value: str) -> ContentType:
		o = ContentType()
		type, params = ParseStringWithParameters()(value)
		o.type = self.strip(type)
		o.charset = self.strip(params['charset']) if 'charset' in params else None
		o.boundary= self.strip(params['boundary']) if 'boundary' in params else None
		return o


class ParseETag(Parse):
	def __call__(self, value: str) -> ETag:
		o = ETag()
		if value[:2] == 'W/':
			o.weakvalidator = True
			value = value[2:]
		o.etag = self.strip(value)
		return o
