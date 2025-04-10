# -*- coding: utf-8 -*-

from Liquirizia.Description import *

from dataclasses import dataclass
from typing import Optional

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
	a: int
	b: int


@dataclass
class QueriesModel:
	a: int
	b: float
	c: str = None


@dataclass
class ContentModel:
	a: int
	b: float


@dataclass
class ArgumentsModel:
	parameters: ParametersModel
	qs: QueriesModel
	content: ContentModel = None


@dataclass
class DataModel:
	message: str
	args: ArgumentsModel
	ret: float


@dataclass
class ResponseModel:
	status: int
	message: str
	data: DataModel = None
