# -*- coding: utf-8 -*-

from Liquirizia.Description import *

from dataclasses import dataclass
from typing import Optional

__all__ = (
	'FORMAT_ARGS',
	'FORMAT_DATA',
)


@dataclass
class Parameters:
	a: int
	b: int


@dataclass
class Query:
	a: int
	b: float
	c: str = None


@dataclass
class Content:
	a: int
	b: float


@dataclass
class Arguments:
	parameters: Parameters
	qs: Query
	content: Content = None


for k, v in Arguments.__annotations__.items():
	print(k, v)

for k, v in Arguments.__dataclass_fields__.items():
	print(k, v)


@dataclass
class Data:
	message: str
	args: Arguments
	ret: float


FORMAT_ARGS = ToSchema(Arguments, name='args')
FORMAT_DATA = ToSchema(Data, name='data')

# FORMAT_ARGS = Schema(
# 	name='args',
# 	format=Object(
# 		properties=Properties(
# 			parameters=Object(
# 				properties=Properties(
# 					a=Integer('파라미터 a'),
# 					b=Integer('파라미터 b'),
# 				)
# 			),
# 			qs=Object(
# 				properties=Properties(
# 					a=Integer('질의 a'),
# 					b=Number('질의 b'),
# 					c=String('질의 c', required=False),
# 				)
# 			),
# 			content=Object(
# 				properties=Properties(
# 					a=Integer('컨텐츠 a'),
# 					b=Number('컨텐츠 b'),
# 				),
# 				required=False,
# 			),
# 		)
# 	)
# )
# 
# FORMAT_DATA = Schema(
# 	name='data',
# 	format=Object(
# 		properties=Properties(
# 			message=String('메세지'),
# 			args=FORMAT_ARGS,
# 			ret=Number('결과값'),
# 		)
# 	)
# )