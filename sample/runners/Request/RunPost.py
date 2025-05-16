# -*- coding: utf-8 -*-

from Liquirizia.WSGI.Properties import *
from Liquirizia.WSGI.Responses import *
from Liquirizia.WSGI.Errors import *
from Liquirizia.WSGI import	Request
from Liquirizia.WSGI.Description import	Response, Content

from Liquirizia.Validator.Patterns import *
from Liquirizia.Validator.Patterns.Object import *
from Liquirizia.Description import *

from ..Session import GetSession
from ..Model import *

__all__ = (
	'RunPost'
)


@RequestProperties(
	method='POST',
	url='/api/run/:a/:b',
	parameter=Parameter(
		{
			'a': ToInteger(IsGreaterThan(100)), 
			'b': ToInteger(IsGreaterThan(100)),
		},
		format={
			'a': Integer('파라미터 a', min=100),
			'b': Integer('파라미터 b', min=100),
		}
	),
	qs=QueryString(
		{
			'a': ToInteger(IsGreaterThan(5)),
			'b': ToNumber(IsGreaterThan(9)),
			'c': (
				SetDefault('안녕'),
				IsString(),
			),
		},
		requires=('a', 'b'),
		format={
			'a': Integer('질의 a', min=5),
			'b': Number('질의 b', min=9),
			'c': String('질의 c', default='안녕', required=False),
		}
	),
	header=Header(
		{
			'X-App-Id': IsToNone(IsString()),
		},
		format={
			'X-App-Id': String(required=False),
		},
	),
	body=Body(
		reader=JavaScriptObjectNotationContentReader(),
		content=IsObject(
			IsRequiredIn('a', 'b'),
			IsMappingOf({
				'a': ToInteger(IsLessThan(5)),
				'b': ToNumber(IsLessThan(9)),
			}),
		),
		format=Object(
			properties=Properties(
				a=Integer('본문 a', max=5),
				b=Number('본문 b', max=9),
			)
		),
		type='application/json',
	),
	response=Response(
		status=200,
		description='성공',
		content=Content(
			format='application/json',
			schema=ToSchema(ResponseModel)
		),
	),
	summary='POST 요청을 처리하는 예제',
	tags='RequestRunner',
)
class RunPost(RequestRunner):
	def __init__(self, request: Request):
		self.request = request
		return

	def run(self, a: int, b: float):
		_ = ResponseModel(
			status=200,
			message='OK',
			data=DataModel(
				message=self.request.qs.c,
				args=ArgumentsModel(
					parameters=ParametersModel(
						a=self.request.parameters.a,
						b=self.request.parameters.b,
					),
					qs=QueriesModel(
						a=self.request.qs.a,
						b=self.request.qs.b,
						c=self.request.qs.c,
					),
					content=ContentModel(
						a=a,
						b=b,
					),
				),
				ret=(self.request.parameters.a + self.request.qs.b + a) * (self.request.parameters.b + self.request.qs.b + b), 
			),
		)
		return ResponseJSON(ToObject(_))
