# -*- coding: utf-8 -*-

from Liquirizia.Description import *

from dataclasses import dataclass
from typing import Annotated, Optional

__all__ = (
	'ParametersModel',
	'QueriesModel',
	'ContentModel',
	'ArgumentsModel',
	'DataModel',
	'ResponseModel',
)


@dataclass
class ParametersModel:
	a: Annotated[int, 'Parameter a']
	b: Annotated[int, 'Parameter b']


@dataclass
class QueriesModel:
	a: Annotated[int, 'Query a']
	b: Annotated[float, 'Query b']
	c: Annotated[Optional[str], 'Query c']


@dataclass
class ContentModel:
	a: Annotated[int, 'Content a']
	b: Annotated[float, 'Content b']


@dataclass
class ArgumentsModel:
	parameters: Annotated[ParametersModel, 'Parameters']
	qs: Annotated[QueriesModel, 'QueryString']
	content: Annotated[Optional[ContentModel], 'Content']


@dataclass
class DataModel:
	message: Annotated[str, 'Message']
	args: Annotated[ArgumentsModel, 'Arguments']
	ret: Annotated[float, 'Return value']


@dataclass
class ResponseModel:
	status: Annotated[int, 'Status code']
	message: Annotated[str, 'Message']
	data: Annotated[Optional[DataModel], 'Data']
