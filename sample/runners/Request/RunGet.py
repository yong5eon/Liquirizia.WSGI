# -*- coding: utf-8 -*-

from Liquirizia.WSGI.Properties import *
from Liquirizia.WSGI.Validators import *
from Liquirizia.WSGI.Authorizations import HTTP
from Liquirizia.WSGI.Responses import *
from Liquirizia.WSGI.Errors import *
from Liquirizia.WSGI import	Request
from Liquirizia.WSGI.Description import	Response, Content

from Liquirizia.Validator.Patterns import *
from Liquirizia.Description import *

from ..Session import GetSession
from ..Model import *

__all__ = (
	'RunGet'
)


@RequestProperties(
	method='GET',
	url='/api/run/:a/:b',
	origin=Origin(all=True),
	auth=HTTP(
		scheme='Bearer',
		format='JWT',
		optional=True,
		auth=GetSession(),
	),
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
	response=Response(
		status=200,
		description='성공',
		content=Content(
			format='application/json',
			schema=ToSchema(ResponseModel)
		),
	),
	summary='GET 요청을 처리하는 예제',
	tags='RequestRunner',
)
class RunGet(RequestRunner):
	def __init__(self, request: Request):
		self.request = request
		return

	def run(self):
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
				),
				ret=(self.request.parameters.a + self.request.qs.b) * (self.request.parameters.b + self.request.qs.b),
			),
		)
		return ResponseJSON(ToObject(_))
