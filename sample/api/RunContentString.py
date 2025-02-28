# -*- coding: utf-8 -*-

from Liquirizia.WSGI.Properties import (
	RequestProperties,
	String as StringValidator,
	RequestRunner,
)
from Liquirizia.WSGI import Request, CORS
from Liquirizia.WSGI.Responses import *
from Liquirizia.WSGI.Errors import BadRequestError
from Liquirizia.WSGI.Description import (
	RequestDescription,
	Body,
	Response,
	Content,
	Object,
	ObjectProperties,
	String,
)

from Liquirizia.Validator.Patterns import *

__all__ = (
	'RunPost'
)


@RequestDescription(
	summary='컨텐츠 검증 샘플 - 문자열',
	description='컨텐츠 검증 샘플 - 문자열',
	tags='RequestRunner - Content Validation',
	body=Body(
		content=(
			Content(
				format='application/json',
				schema=String(),
				example='',
			),
			Content(
				format='application/x-www-form',
				schema=String(),
				example='',
			),
		),
	),
	responses=(
		Response(
			status=200,
			description='완료',
			content=Content(
				format='application/json',
				schema=Object(
					properties=ObjectProperties(
						content=String(),
					),
				),
				example={
					'content': '',
				},
			),
		),
	),
	order=4,
)
@RequestProperties(
	method='POST',
	url='/api/content/string',
	cors=CORS(
		headers=[
			'Content-Type',
			'Content-Length',
		],
	),
	content=StringValidator(
		required=True,
		error=BadRequestError('잘못된 본문 정보 입니다.'),
	),
)
class RunPost(RequestRunner):
	def __init__(self, request: Request):
		self.request = request
		return

	def run(self, content: bool):
		return ResponseJSON({
			'content': content
		})
