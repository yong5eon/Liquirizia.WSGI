# -*- coding: utf-8 -*-

from Liquirizia.WSGI.Properties import (
	RequestProperties,
	Array as ArrayValidator,
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
	Array,
)

from Liquirizia.Validator.Patterns import *

__all__ = (
	'RunPost'
)


@RequestDescription(
	summary='컨텐츠 검증 샘플 - 배열',
	description='컨텐츠 검증 샘플 - 배열',
	tags='RequestRunner - Content Validation',
	body=Body(
		content=(
			Content(
				format='application/json',
				schema=Array(),
				example=[],
			),
			Content(
				format='application/x-www-form',
				schema=Array(),
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
						content=Array(),
					),
				),
				example={
					'content': [],
				},
			),
		),
	),
)
@RequestProperties(
	method='POST',
	url='/api/content/array',
	cors=CORS(
		headers=[
			'Content-Type',
			'Content-Length',
		],
	),
	content=ArrayValidator(
		required=True,
		error=BadRequestError('잘못된 본문 정보 입니다.'),
	),
)
class RunPost(RequestRunner):
	def __init__(self, request: Request):
		self.request = request
		return

	def run(self, *content):
		return ResponseJSON({
			'content': content
		})
