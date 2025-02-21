# -*- coding: utf-8 -*-

from Liquirizia.WSGI.Properties import (
	RequestProperties,
	Boolean as BooleanValidator,
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
	Boolean,
)

from Liquirizia.Validator.Patterns import *

__all__ = (
	'RunPost'
)


@RequestDescription(
	summary='컨텐츠 검증 샘플 - 불리언',
	description='컨텐츠 검증 샘플 - 불리언',
	tags='RequestRunner - Content',
	body=Body(
		content=(
			Content(
				format='application/json',
				schema=Boolean(),
				example=True,
			),
			Content(
				format='application/x-www-form',
				schema=Boolean(),
				example=True,
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
						content=Boolean(),
					),
				),
				example={
					'content': True,
				},
			),
		),
	),
)
@RequestProperties(
	method='POST',
	url='/api/content/bool',
	cors=CORS(
		headers=[
			'Content-Type',
			'Content-Length',
		],
	),
	content=BooleanValidator(
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
