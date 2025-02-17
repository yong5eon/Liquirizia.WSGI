# Liquirizia.WSGI

WSGI(Web Server Gateway Interface)

## 지원

- 어플리케이션 요청에 대한 처리 서빙
- 파일 서빙
- 파일 시스템 서빙 

### 어플리케이션 요청 처리 서빙 방법(Liquirizia.WSGI.Properties) 

- Liquirizia.WSGI.Properties.RequestRunner
- Liquirizia.WSGI.Properties.RequestStreamRunner
- Liquirizia.WSGI.Properties.RequestServerSentEventsRunner
- Liquirizia.WSGI.Properties.RequestWebSocketRunner

### 본문 요청 파서(Liquirizia.WSGI.Parser)

- application/x-www-form-urlencoded : Liquirizia.WSGI.Parser.FormUrlEncodedParser
- application/json: Liquirizia.WSGI.Parser.JavaScriptObjectNotationParser


## 샘플

- [어플리케이션](sample/sample.py)

### 일반적인 형태의 요청 처리

- [GET](sample/api/RunGet.py)
- [POST](sample/api/RunPost.py)
- [PUT](sample/api/RunPut.py)
- [DELETE](sample/api/RunDelete.py)

### 스트림 형태의 요청 처리

- [스트림 입력](sample/api/RunStreamIn.py)
- [스트림 출력](sample/api/RunStreamOut.py)
- [청크 스트림 입력](sample/api/RunChunkedStreamIn.py)
- [청크 스트림 출력](sample/api/RunChunkedStreamOut.py)
- [서버 전송 이벤트](sample/api/RunServerSentEvent.py)

### 양방향 통신 형태의 요청 처리

- [웹소켓](sample/api/RunWebSocket.py)

## 서빙

### 내부 서빙 함수를 통한 서빙

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

### 구니콘(Gunicorn)을 통한 서빙

```shell
> gunicorn path.to.module.application --worker-class=[sync|gevent|eventlet|greenlet]
```

### 구니콘(Gunicorn)과 유비콘 워커(UvicornWorker)를 통한 서빙

```python
from uvicorn.workers import UvicornWorker

class Worker(UvicornWorker):
  CONFIG_KWARGS = {
    "interface": "wsgi",
    "http": "auto",
    "lifespan": "off",
  }
```

## VSCode 환경설정

### 내부 서빙 함수

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

### 구니콘(Gunicorn)

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

- [파일 및 파일 시스템 서빙](docs/ServeFile.md)
- [요청 본문 파서 확장](docs/Parser.md)
- [OAS(OpenAPI Specification)를 사용한 문서화](docs/Documentation.md)

## 참고

- [PEP 3333 – Python Web Server Gateway Interface v1.0.1](https://peps.python.org/pep-3333/)
- [Python WSGI Utilities and Reference Implementation](https://docs.python.org/ko/3/library/wsgiref.html)
- [Gunicorn Documents](https://gunicorn.org/#docs)
