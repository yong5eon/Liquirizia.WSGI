# -*- coding: utf-8 -*-

from ..Response import Response

from Liquirizia.Serializer import SerializerHelper

from typing import Dict, Any, Mapping

__all__ = (
	'ResponseText'
	'ResponseHTML'
	'ResponseJSON'
)

class ResponseText(Response):
	"""Response HTML Class"""
	def __init__(self, body: str, status=200, message='OK', headers: Dict[str, Any] = {}):
		body = SerializerHelper.Encode(body, 'text/plain', 'utf-8')
		super(ResponseHTML, self).__init__(
			status=status,
			message=message,
			headers=headers,
			body=body,
			format='text/plain',
			charset='utf-8',
		)
		return


class ResponseHTML(Response):
	"""Response HTML Class"""
	def __init__(self, body: str, status=200, message='OK', headers: Dict[str, Any] = {}):
		body = SerializerHelper.Encode(body, 'text/html', 'utf-8')
		super(ResponseHTML, self).__init__(
			status=status,
			message=message,
			headers=headers,
			body=body,
			format='text/html',
			charset='utf-8',
		)
		return


class ResponseJSON(Response):
	"""Response JSON Class"""
	def __init__(self, body: Mapping, status=200, message='OK', headers: Dict[str, Any ]= {}):
		body = SerializerHelper.Encode(body, 'application/json', 'utf-8')
		super().__init__(
			status=status,
			message=message,
			headers=headers,
			body=body,
			format='application/json',
			charset='utf-8',
		)
		return
