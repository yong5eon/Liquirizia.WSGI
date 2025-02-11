# -*- coding: utf-8 -*-

from datetime import datetime

__all__ = (
	'ToDate',
	'ToDatetime',
)

def ToDate(dt: datetime) -> str:
	return dt.strftime('%a, %d %b %Y %H:%M:%S GMT')

def ToDatetime(dt: str) -> datetime:
	# TODO : support timezone
	return datetime.strptime(dt, '%a, %d %b %Y %H:%M:%S GMT')

print(ToDate(datetime.now()))
print(ToDatetime('Tue, 11 Feb 2025 18:00:18 GMT'))