# -*- coding: utf-8 -*-

from Liquirizia.Test import *
from Liquirizia.WSGI.Utils import (
	ParseBoolean,
	ParseString,
	ParseStringWithParameters,
	ParseInteger,
	ParseFloat,
	ParseDate,
	ParseParameter,
	ParseParameters,
	ParseList,
	ParseJSON,
)


class TestParse(Case):
	@Parameterized(
		{'i': '1', 'o': True},
		{'i': '0', 'o': None},
		{'i': '2', 'o': None},
	)
	@Order(0)
	def testParseBoolean(self, i, o):
		_ = ParseBoolean()(i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': 'application/json; charset=utf-8', 'o': 'application/json; charset=utf-8'},
	)
	@Order(1)
	def testParseString(self, i, o):
		_ = ParseString()(i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': 'application/json; charset=utf-8', 'o': 'application/json', 'params': {'charset': 'utf-8'}},
	)
	@Order(2)
	def testParseStringWithParameters(self, i, o, params):
		_, parameters = ParseStringWithParameters()(i)
		ASSERT_IS_EQUAL(_, o)
		ASSERT_IS_EQUAL(parameters, params)
		return

	@Parameterized(
		{'i': '1', 'o': 1},
		{'i': '1.0', 'o': 1},
		{'i': '0', 'o': 0},
	)
	@Order(3)
	def testParseInteger(self, i, o):
		_ = ParseInteger()(i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': '1', 'o': 1.0},
		{'i': '1.0', 'o': 1.0},
		{'i': '0', 'o': 0.0},
	)
	@Order(4)
	def testParseFloat(self, i, o):
		_ = ParseFloat()(i)
		ASSERT_IS_EQUAL(_, o)
		return
	
	@Parameterized(
		{'i': 'Tue, 29 Oct 2024 16:56:32 GMT', 'o': None},
	)
	@Order(5)
	def testParseDate(self, i, o):
		from datetime import datetime
		_ = ParseDate()(i)
		ASSERT_IS_EQUAL(isinstance(_, datetime), True)
		return
	
	@Parameterized(
		{'i': 'a=1', 'o': ('a', '1')},
		{'i': 'a', 'o': ('a', None)},
	)
	@Order(6)
	def testParseParameter(self, i, o):
		_ = ParseParameter()(i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': 'a=1,b=s,c=2.0', 'o': {'a':'1','b':'s','c':'2.0'}},
		{'i': 'a=1,b=s,c', 'o': {'a':'1','b':'s','c':None}},
	)
	@Order(7)
	def testParseParameters(self, i, o):
		_ = ParseParameters()(i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': 'a=1,b=s,c=2.0', 'o': ['a=1','b=s','c=2.0']},
	)
	@Order(8)
	def testParseList(self, i, o):
		_ = ParseList()(i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': 'a=1 b=s c=2.0,a=1 b=s c=2.0', 'o': [{'a':'1','b':'s','c':'2.0'},{'a':'1','b':'s','c':'2.0'}]},
	)
	@Order(9)
	def testParseListWithParseParameters(self, i, o):
		_ = ParseList(fetch=ParseParameters(sep=' '))(i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{
			'i': 'application/json; charset=utf-8, text/plain; charset=utf-8', 
			'o': [
				('application/json',{'charset':'utf-8'}),
				('text/plain',{'charset':'utf-8'}),
			]
		},
	)
	@Order(10)
	def testParseListWithParseStringWithParameters(self, i, o):
		_ = ParseList(fetch=ParseStringWithParameters())(i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': '{"a":1,"b":"str","c":1.0}', 'o': {'a':1,'b':'str','c':1.0}},
	)
	@Order(11)
	def testAttributionReporingTrigger(self, i, o):
		_ = ParseJSON()(i)
		ASSERT_IS_EQUAL(_, o)
		return
