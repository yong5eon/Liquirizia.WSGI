# -*- coding: utf-8 -*-

from Liquirizia.Description import *

__all__ = (
	'FORMAT_ARGS',
	'FORMAT_DATA',
)


FORMAT_ARGS = Schema(
	name='args',
	format=Object(
		properties=Properties(
			parameters=Object(
				properties=Properties(
					a=Integer('파라미터 a'),
					b=Integer('파라미터 b'),
				)
			),
			qs=Object(
				properties=Properties(
					a=Integer('질의 a'),
					b=Number('질의 b'),
				)
			),
			content=Object(
				properties=Properties(
					a=Integer('컨텐츠 a'),
					b=Number('컨텐츠 b'),
				),
				required=False,
			),
		)
	)
)

FORMAT_DATA = Schema(
	name='data',
	format=Object(
		properties=Properties(
			message=String('메세지'),
			args=FORMAT_ARGS,
			ret=Number('결과값'),
		)
	)
)