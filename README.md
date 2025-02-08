# Liquirizia.WSGI

WSGI(Web Server Gateway Interface)

## Development

- [Application Sample](sample/sample.py)

### Controllers

- [GET Controller](sample/api/RunGet.py)
- [POST Controller](sample/api/RunPost.py)
- [PUT Controller](sample/api/RunPut.py)
- [DELETE Controller](sample/api/RunDelete.py)

### Stream Controllers

- [Stream In](sample/api/RunStreamIn.py)
- [Stream Out](sample/api/RunStreamOut.py)
- [Chunked Stream In](sample/api/RunChunkedStreamIn.py)
- [Chunked Stream Out](sample/api/RunChunkedStreamOut.py)
- [Server Sent Event](sample/api/RunServerSentEvent.py)
- [WebSocket](sample/api/RunWebSocket.py)

## Run

### Run with serve

```python
from Liquirizia.WSGI import (
  Application,
  serve,
)

aps = Application(
  ...
)

with serve('127.0.0.1', 8000, aps) as httpd:
  httpd.serve_forever()
```

### Run with Gunicorn

```shell
> gunicorn path.to.module.application --worker-class=[sync|gevent|eventlet|greenlet]
```

### Run With Gunicorn + Uvicorn

```python
from uvicorn.workers import UvicornWorker

class Worker(UvicornWorker):
  CONFIG_KWARGS = {
    "interface": "wsgi",
    "http": "auto",
    "lifespan": "off",
  }
```

## Launch Configuration for VSCode

### With Liquirizia.WSGI.serve

```json
...
{
  "name": "${NAME}",
  "type": "debugpy",
  "request": "launch",
  "cwd": "/path/to",
  "program": "${FILE}.py",
  "console": "integratedTerminal",
  "justMyCode": true,
  "env": {
  "PYTHONPATH": "/path/to"
  }
},
...
```

### With Gunicorn

```json
{
  "name": "- API-Chat",
  "type": "debugpy",
  "request": "launch",
  "cwd": "/path/to",
  "module": "gunicorn",
  "args": "${MODULE}:${APPLICATION} --reload --log-level=${LOG_LEVEL} --timeout=${TIMEOUT} --keep-alive=${KEEP_ALIVE} --worker-class=${WORKER_CLASS}",
  "console": "integratedTerminal",
  "justMyCode": true,
  "env": {
  "GEVENT_SUPPORT": "true",
  }
},
```

## 기타

- [OAS(OpenAPI Specification)를 사용한 문서화](docs/Documentation.md)

## 참고

- [PEP 3333 – Python Web Server Gateway Interface v1.0.1](https://peps.python.org/pep-3333/)
- [Python WSGI Utilities and Reference Implementation](https://docs.python.org/ko/3/library/wsgiref.html)
- [Gunicorn Documents](https://gunicorn.org/#docs)
