# -*- coding: utf-8 -*-

from Liquirizia.WSGI.Properties import *
from Liquirizia.WSGI.Responses import *
from Liquirizia.WSGI.Errors import *
from Liquirizia.WSGI import	Request
from Liquirizia.WSGI.Description import Descriptor, Tag, Response, Content
from Liquirizia.Description import *

from .Model import *

__all__ = (
	'RunGetDocument'
)


@RequestProperties(
	method='GET',
	url='/api/doc',
	response=Response(
		status=200,
		description='성공',
		content=Content(
			format='application/json',
			schema=Object(),
		),
	),
	tags='Common',
)
class RunGet(RequestRunner):
	def __init__(self, request: Request):
		self.request = request
		return

	def run(self):
		return ResponseJSON(Descriptor().toDocument(
			tags=(
				Tag('RequestRunner', description='일반적인 요청 처리 예제'),
				Tag('RequestStreamRunner', description='스트림 요청 처리 예제'),
				Tag('RequestStreamRunner - Chunked', description='청크 스트림 요청 처리 예제'),
				Tag('RequestServerSentEventsRunner', description='Server-Sent Events 요청 처리 예제'),
				Tag('RequestWebSocketRunner', description='WebSocket 요청 처리 예제'),
				Tag('Content Validation', description='일반적인 요청 처리 시 본문으로 전달되는 컨텐츠의 유효성 검사 예제'),
				Tag('Auth', description='인증 처리 예제'),
				Tag('Common'),
			),
			schemas=(
				ToSchema(ParametersModel),
				ToSchema(QueriesModel),
				ToSchema(ContentModel),
				ToSchema(ArgumentsModel),
				ToSchema(DataModel),
				ToSchema(ResponseModel),
			),
			sortUrl=lambda url: {
				'/api/content/bool': '11',
				'/api/content/integer': '12',
				'/api/content/number': '13',
				'/api/content/string': '14',
				'/api/content/array': '14',
				'/api/content/object': '14',
			}.get(url, '99'),
			sortMethod=lambda o: {
				'POST': 1,
				'GET': 2,
				'PUT': 3,
				'DELETE': 4,
			}.get(o.upper(), 9),
		))
