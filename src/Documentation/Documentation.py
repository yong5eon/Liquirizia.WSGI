# -*- coding: utf-8 -*-

from collections.abc import MutableMapping
from typing import ItemsView, Iterator, KeysView, ValuesView, Any

__all__ = (
	'Documentation',
)


class Documentation(MutableMapping):
	def __init__(self, **kwargs):
		self.__document__ = kwargs
		return

	def __getitem__(self, key: Any) -> Any:
		return self.__document__.__getitem__(key)
	
	def __setitem__(self, key: Any, value: Any) -> None:
		return self.__document__.__setitem__(key, value)
	
	def __delitem__(self, key: Any) -> None:
		return self.__document__.__delitem__(key)
	
	def __iter__(self) -> Iterator:
		return self.__document__.__iter__()
	
	def __len__(self) -> int:
		return self.__document__.__len__()
	
	def __contains__(self, key: object) -> bool:
		return self.__document__.__contains__(key)
	
	def keys(self) -> KeysView:
		return self.__document__.keys()
	
	def items(self) -> ItemsView:
		return self.__document__.items()
	
	def values(self) -> ValuesView:
		return self.__document__.values()
	
	def __eq__(self, other: object) -> bool:
		return self.__document__.__eq__(other)
	
	def __ne__(self, value: object) -> bool:
		return self.__document__.__ne__(value)
	
	def get(self, key: object) -> Any:
		return self.__document__.get(key)
	