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
)


class FormatError(Schema):
	def __init__(self):
		super().__init__(
			name='Error',
			format=String('에러 메세지'),
		)
		return


class FormatRequest(Schema):
	def __init__(self):
		super().__init__(
			name='Request',
			format=Object(
				properties=ObjectProperties(
					a=Integer('파라미터 a'),
					b=Number('파라미터 b'),
				),
			),
		)
		return


class FormatResponse(Schema):
	def __init__(self):
		super().__init__(
			name='Response',
			format=Object(
				properties=ObjectProperties(
					status=Integer('상태'),
					message=String('메세지'),
					data=Object(
						properties=ObjectProperties(
							message=String('응답 메세지'),
							res=Object(
								properties=ObjectProperties(
									parameters=Object(
										properties=ObjectProperties(
											a=Integer('파라미터 a'),
											b=Number('파라미터 b'),
										),
										description='파라미터',
									),
									qs=Object(
										properties=ObjectProperties(
											a=Integer('쿼리스트링 a'),
											b=Number('쿼리스트링 b'),
										),
										description='쿼리스트링',
									),
									content=Object(
										properties=ObjectProperties(
											a=Integer('컨텐트 a'),
											b=Number('컨텐트 b'),
										),
										description='컨텐트',
									)
								),
								description='응답 결과',
								requires=('parameters', 'qs'),
							)
						),
						description='응답 데이터',
					)
				),
				description='응답',
				requires=('status', 'message', 'data'),
			),
		)
		return
