# -*- coding: utf-8 -*-

from dataclasses import make_dataclass, fields
from typing import Any, Dict

__all__ = (
	'ObjectToDataObject',
)


def ObjectToDataObject(name: str, data: Dict[str, Any]) -> Any:
	values = [(key, type(value)) for key, value in data.items()]
	o = make_dataclass(name, values)
	names = {f.name for f in fields(o)}
	kwargs = {k: v for k, v in data.items() if k in names}
	return o(**kwargs)
