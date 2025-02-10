# 요청 본문 파서 확장 지원

```python
from Liquirizia.WSGI import RequestProperties
from Liquirizia.WSGI.Properties import RequestRunner
from Liquirizia.WSGI import Requet, Response, Parser

from json import loads

from typing import Dict, Any


class SampleParser(Parser):
	def __call__(self, body: str) -> Dict[str, Any]:
		try:
			return loads(body)
		except:
			raise ValueError('json parse error')

@RequestProperties(
	method='POST',
	uri='/path/to',
	...
	bodyParsers={
		'application/json': SampleParser(),
	},
	...
)
class SampleRunner(RequestRunner):
	def __init__(self, request: Request):
		self.request = request
		return
	def run(self):
		...
		return Response(200, 'OK')
```
