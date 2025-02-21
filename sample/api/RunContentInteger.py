# -*- coding: utf-8 -*-

from Liquirizia.WSGI.Properties import (
	RequestProperties,
	Integer as IntegerValidator,
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
	Integer,
)

from Liquirizia.Validator.Patterns import *

__all__ = (
	'RunPost'
)


@RequestDescription(
	summary='컨텐츠 검증 샘플 - 정수',
	description='컨텐츠 검증 샘플 - 정수',
	tags='RequestRunner - Content',
	body=Body(
		content=(
			Content(
				format='application/json',
				schema=Integer(),
				example=0,
			),
			Content(
				format='application/x-www-form',
				schema=Integer(),
				example=0,
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
						content=Integer(),
					),
				),
				example={
					'content': 0,
				},
			),
		),
	),
)
@RequestProperties(
	method='POST',
	url='/api/content/integer',
	cors=CORS(
		headers=[
			'Content-Type',
			'Content-Length',
		],
	),
	content=IntegerValidator(
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
