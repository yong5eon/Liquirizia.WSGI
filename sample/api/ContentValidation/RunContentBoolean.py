# -*- coding: utf-8 -*-

from Liquirizia.WSGI.Properties import RequestRunner
from Liquirizia.WSGI import (
	RequestProperties,
	Request,
)
from Liquirizia.WSGI.Validator import *
from Liquirizia.WSGI.Validators import *
from Liquirizia.WSGI.Decoders import *
from Liquirizia.WSGI.Responses import *
from Liquirizia.WSGI.Errors import BadRequestError

__all__ = (
	'RunPost'
)


@RequestDescription(
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

)
@RequestProperties(
	method='POST',
	url='/api/content/bool',
	content=BooleanValidator(
		required=True,
		error=BadRequestError('잘못된 본문 정보 입니다.'),
	),
	summary='컨텐츠 검증 샘플 - 불리언',
	description='컨텐츠 검증 샘플 - 불리언',
	tags='RequestRunner - Content Validation',
)
class RunPost(RequestRunner):
	def __init__(self, request: Request):
		self.request = request
		return

	def run(self, content: bool):
		return ResponseJSON({
			'content': content
		})
