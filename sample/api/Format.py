# -*- coding: utf-8 -*-

from Liquirizia.WSGI.Description import (
	Schema,
	Integer,
	Number,
	String,
	Array,
	Object,
	ObjectProperties,
)

__all__ = (
	'FormatError',
	'FormatRequest',
	'FormatResponse',
	'FormatData',
	'FormatParameters',
	'FormatQueryString',
	'FormatContent',
	'FormatExtra',
)


FormatError = Schema(
	name='Error',
	format=String('에러 메세지'),
)

FormatRequest = Schema(
	name='Request',
	format=Object(
		properties=ObjectProperties(
			a=Integer('파라미터 a'),
			b=Number('파라미터 b'),
		),
	),
)

FormatParameters = Schema(
	name='Parameters',
	format=Object(
		properties=ObjectProperties(
			a=Integer('a'),
			b=Number('b'),
		),
		requires=('a', 'b'),
		description='파라미터',
	),
)

FormatQueryString = Schema(
	name='QueryString',
	format=Object(
		properties=ObjectProperties(
			a=Integer('a'),
			b=Number('b'),
		),
		requires=('a', 'b'),
		description='쿼리스트링',
	),
)

FormatContent = Schema(
	name='Content',
	format=Object(
		properties=ObjectProperties(
			a=Integer('a'),
			b=Number('b'),
		),
		requires=('a', 'b'),
		description='컨텐츠',
	),
)

FormatData = Schema(
	name='Data',
	format=Object(
		properties=ObjectProperties(
			message=String('응답 메세지'),
			res=Object(
				properties=ObjectProperties(
					parameters=FormatParameters,
					qs=FormatQueryString,
					content=FormatContent
				),
				requires=('parameters', 'qs'),
				description='응답 결과',
			),
		),
		requires=('message', 'res'),
		description='데이터',
	),
)

FormatExtra = Schema(
	name='Extra',
	format=Object(
		properties=ObjectProperties(
			a=Integer('a'),
			b=Number('b'),
		),
		description='추가 데이터',
	),
)

FormatResponse = Schema(
	name='Response',
	format=Object(
		properties=ObjectProperties(
			status=Integer('상태'),
			message=String('메세지'),
			data=FormatData,
			extras=Array(
				format=FormatExtra,
				description='추가 데이터 리스트',
				required=False,
			),
		),
		description='응답',
		requires=('status', 'message', 'data'),
	),
)
