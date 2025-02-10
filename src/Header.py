# -*- coding: utf-8 -*-

from re import match

__all__ = (
	'Header',
)


class Header(object):
	"""Header Class"""
	def __init__(self, value: str):
		self.value = value
		return
	def __str__(self): return self.value


# https://www.iana.org/assignments/http-fields/http-fields.xhtml
# https://developer.mozilla.org/ko/docs/Web/HTTP/Headers 
#
# HTTP Types
# - Request Header
# - Response Header
# - Representation(Entity) Headers
# - Payload Headers
#
# Header Structures 
# - String
# - Structured
#   - List
#   - Dict
#   - Item
#   - Token


class ContentType(Header):
	"""Content-Type Header Class"""
	def __init__(self, value: str):
		super().__init__(value)
		self.format, self.params = self.parse(value)
		return

	def parse(self, value: str):
		parts = value.split(';', 1)
		format = parts[0].strip()
		params = {}
		for part in parts[1:]:
			if '=' in part:
				k, v = part.split('=', 1)
				params[k.strip()] = v.strip()
		return format, params


class Accept(Header):
	"""Accept Header Class"""
	def __init__(self, value: str):
		super().__init__(value)
		self.params = self.parse(value)
		return
	def parse(self, value: str):
		"""Split mime-type and q"""
		parts = value.split(",")
		parsed = []
		for part in parts:
			m = match(r'([^;]+)(?:;\s*q=([\d.]+))?', part.strip())
			if m:
				t = m.group(1).strip()
				q = float(m.group(2)) if m.group(2) else 1.0
				parsed.append({"type": t, "q": q})
		return sorted(parsed, key=lambda x: x["q"], reverse=True)
	def match(self, min=1.0):
		pass
