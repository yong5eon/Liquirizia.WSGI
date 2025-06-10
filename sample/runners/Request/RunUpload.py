# -*- coding: utf-8 -*-

from Liquirizia.WSGI.Properties import *
from Liquirizia.WSGI.Responses import *
from Liquirizia.WSGI.Errors import *
from Liquirizia.WSGI import	Request
from Liquirizia.WSGI.Description import	Response, Content

from Liquirizia.Validator.Patterns import *
from Liquirizia.Validator.Patterns.Object import *
from Liquirizia.Description import *

from ..Model import *

__all__ = (
	'RunUpload'
)


@RequestProperties(
	method='POST',
	url='/api/run/upload',
	headers=Headers(
		{
			'Content-Format': IsString(),
			'Content-Charset': IsToNone(IsString()),
		},
		requires=['Content-Format'],
		format={
			'Content-Format': String(),
			'Content-Charset': String(required=False),
		},
	),
	body=Body(
		reader=ByteArrayContentReader(),
		content=Content(
			format='application/octet-stream',
			schema=Binary(),
		),
	),
	response=Response(
		status=200,
		description='성공',
		content=Content(
			format='*/*',
			schema=Binary()
		),
	),
	summary='POST 파일 업로드를 처리하는 예제',
	tags='RequestRunner',
)
class RunUpload(RequestRunner):
	def __init__(self, request: Request):
		self.request = request
		return

	def run(self, buffer: bytes):
		return ResponseBuffer(
			status=200,
			buffer=buffer,
			size=len(buffer),
			format=self.request.header('Content-Format'),
			charset=self.request.header('Content-Charset'),
		)
