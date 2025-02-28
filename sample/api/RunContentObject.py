# -*- coding: utf-8 -*-

from Liquirizia.WSGI.Properties import (
	RequestProperties,
	Object as ObjectValidator,
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
)

from Liquirizia.Validator.Patterns import *

__all__ = (
	'RunPost'
)


@RequestDescription(
	summary='컨텐츠 검증 샘플 - 객체',
	description='컨텐츠 검증 샘플 - 객체',
	tags='RequestRunner - Content Validation',
	body=Body(
		content=(
			Content(
				format='application/json',
				schema=Object(properties=ObjectProperties()),
				example=[],
			),
			Content(
				format='application/x-www-form',
				schema=Object(properties=ObjectProperties()),
				example=[],
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
						content=Object(properties=ObjectProperties()),
					),
				),
				example={
					'content': {},
				},
			),
		),
	),
	order=6,
)
@RequestProperties(
	method='POST',
	url='/api/content/object',
	cors=CORS(
		headers=[
			'Content-Type',
			'Content-Length',
		],
	),
	content=ObjectValidator(
		required=True,
		error=BadRequestError('잘못된 본문 정보 입니다.'),
	),
)
class RunPost(RequestRunner):
	def __init__(self, request: Request):
		self.request = request
		return

	def run(self, **content):
		return ResponseJSON({
			'content': content
		})
