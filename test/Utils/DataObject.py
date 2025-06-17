# -*- coding: utf-8 -*-

from Liquirizia.Test import *

from Liquirizia.WSGI.Utils.DataObject import (
	ObjectToDataObject,
)

from typing import Dict, Any

class TestUtilsDictionary(Case):
	@Parameterized(
		{'name': 'TestObject', 'i': {'a': 1, 'b': 2.0, 'c': 'str', 'd': [1,2,3], 'e': (1,2), 'f': {1,3,3}, 'g': {'a': 1, 'b': 2.0, 'c': 'str'}}}
	)
	def test(self, name, i: Dict[str, Any]):
		_ = ObjectToDataObject(name, i)
		for k, v in i.items():
			ASSERT_TRUE(hasattr(_, k))
			ASSERT_IS_EQUAL(getattr(_, k), v)
		return
