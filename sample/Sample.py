# -*- coding: utf-8 -*-

from Liquirizia.WSGI import (
		Application, 
		Handler,
		Request,
		Response,
		Error,
		serve,
)
from Liquirizia.WSGI.Responses import *
from Liquirizia.WSGI.Properties import RequestFilter
from Liquirizia.WSGI.Description import Descriptor, Information, Contact, Tag
from Liquirizia.WSGI.Utils import Load

from Liquirizia.FileSystemObject import Helper as FileSystemObjectHelper
from Liquirizia.FileSystemObject.Implements.FileSystem import (
		Configuration as FileSystemObjectConfiguration, 
		Connection as FileSystemObject,
)


from Filters import ToJPEG

from os.path import dirname, realpath
from sys import stderr
from traceback import format_tb
from datetime import datetime

PATH = dirname(realpath(__file__))

FileSystemObjectHelper.Set(
	'Sample',
	FileSystemObject,
	FileSystemObjectConfiguration('res/images')
)

class SampleHandler(Handler):
	def onRequest(self, request: Request):
		print('{} - {} - REQUEST  - {} - {} - {} - {} - {} - {}'.format(
			datetime.now().isoformat(),
			request.id[:16],
			request.remote,
			str(request),
			request.parameters,
			request.qs,
			request.header('Content-Type'),
			request.size,
		))
		for k, _ in request.headers():
			print('{} - {}'.format(k, request.header(k)))
		return request, None
	def onRequestResponse(self, request: Request, response: Response):
		print('{} - {} - RESPONSE - {} - {} - {}'.format(
			datetime.now().isoformat(),
			request.id[:16],
			request.remote,
			str(response),
			response.size
		))
		for k, _ in response.headers():
			print('{} - {}'.format(k, response.header(k)))
		return response
	def onRequestComplete(self, request: Request):
		print('{} - {} - DONE     - {} - {}'.format(
			datetime.now().isoformat(),
			request.id[:16],
			request.remote,
			str(request)
		))
		return
	def onRequestError(self, request: Request, error: Error):
		print('{} - {} - ERROR    - {} - {}'.format(
			datetime.now().isoformat(),
			request.id[:16],
			request.remote,
			str(request)
		))
		tb = str(error)
		tb += '\n'
		tb += ''.join(format_tb(error.__traceback__)).strip().replace(' ' * 4, ' ' * 2)
		print(tb)
		return ResponseText(
			text=tb,
			status=error.status,
			message=error.message,
			headers=error.headers,
		)
	def onRequestException(self, request: Request, e: Exception):
		print('{} - {} - EXCEPT   - {} - {}'.format(
			datetime.now().isoformat(),
			request.id[:16],
			request.remote,
			str(request)
		))
		tb = str(e)
		tb += '\n'
		tb += ''.join(format_tb(e.__traceback__)).strip().replace(' ' * 4, ' ' * 2)
		print(tb)
		return ResponseBadRequest(body=tb.encode(), format='text/plain', charset='utf-8')
	def onError(self, env, error: Error):
		print('{} - {} - ERROR   - {} - {} {} - {}'.format(
			datetime.now().isoformat(),
			env['REQUEST_ID'][:16],
			env['REMOTE_ADDR'],
			env['REQUEST_METHOD'],
			env['PATH_INFO'],
			str(error)
		))
		tb = str(error)
		tb += '\n'
		tb += ''.join(format_tb(error.__traceback__)).strip().replace(' ' * 4, ' ' * 2)
		print(tb)
		return ResponseText(
			text=tb,
			status=error.status,
			message=error.message,
			headers=error.headers,
		)
	def onException(self, env, e: Exception):
		print('{} - {} - EXCEPT  - {} - {} {} - {}'.format(
			datetime.now().isoformat(),
			env['REQUEST_ID'][:16],
			env['REMOTE_ADDR'],
			env['REQUEST_METHOD'],
			env['PATH_INFO'],
			str(e)
		))
		tb = str(e)
		tb += '\n'
		tb += ''.join(format_tb(e.__traceback__)).strip().replace(' ' * 4, ' ' * 2)
		print(tb)
		return ResponseServiceUnavailable(body=tb.encode(), format='text/plain', charset='utf-8')


aps = Application(
	handler=SampleHandler(),
	headers={
		'X_APP_ID': 'X-App-Id',
		'CREDENTIALS': 'Credentials',
		'CONTENT_FORMAT': 'Content-Format',
		'CONTENT_CHARSET': 'Content-Charset',
	},
)

from Liquirizia.WSGI.Description import *
from Liquirizia.Description import *

descriptor = Descriptor(
	info=Information(
		title='Liquirizia.WSGI Sample API',
		version=open('../VERSION', 'rt').read().strip(),
		summary='Sample API Document',
		description='Sample API',
		contact=Contact(
			name='Heo Yongseon',
			url='https://github.com/yong5eon/Liquirizia.WSGI',
			email='contact@email.com'
		)
	),
	errorResponses=(
		Response(
			status=400,
			description='잘못된 요청',
			content=Content(
				format='text/plain',
				schema=String('원인')
			)
		),
	),
	authErrorResponses=(
		Response(
			status=401,
			description='인증 실패',
			content=Content(
				format='text/plain',
				schema=String('원인')
			)
		),
		Response(
			status=403,
			description='권한 없음',
			content=Content(
				format='text/plain',
				schema=String('원인')
			)
		),
	),
)

Load(mod='runners')

# import model
from Liquirizia.Description import ToSchema
from runners.Model import *
# apply swagger-ui
import sys
import DocumentHandler

from swagger_ui import supported_list, api_doc

sys.modules['swagger_ui.handlers.Liquirizia'] = DocumentHandler
supported_list.append('Liquirizia')

api_doc(
	aps,
	config=Descriptor().toDocument(
		tags=(
			Tag('RequestRunner', description='일반적인 요청 처리 예제'),
			Tag('RequestStreamRunner', description='스트림 요청 처리 예제'),
			Tag('RequestStreamRunner - Chunked', description='청크 스트림 요청 처리 예제'),
			Tag('RequestServerSentEventsRunner', description='Server-Sent Events 요청 처리 예제'),
			Tag('RequestWebSocketRunner', description='WebSocket 요청 처리 예제'),
			Tag('Content Validation', description='일반적인 요청 처리 시 본문으로 전달되는 컨텐츠의 유효성 검사 예제'),
			Tag('Auth', description='인증 처리 예제'),
			Tag('Common'),
		),
		schemas=(
			ToSchema(ParametersModel, description='Parameter'),
			ToSchema(QueriesModel, description='QueryString'),
			ToSchema(ContentModel, description='Content'),
			ToSchema(ArgumentsModel, description='Arguments'),
			ToSchema(DataModel, description='Data'),
			ToSchema(ResponseModel, description='Response'),
		),
		sortUrl=lambda url: {
			# request runner
			'/api/run/:a/:b': 1,
			'/api/run/upload': 2,
			# content validation
			'/api/content/bool': 1,
			'/api/content/integer': 2,
			'/api/content/number': 3,
			'/api/content/string': 4,
			'/api/content/array': 5,
			'/api/content/object': 6,
			# auth
			'/api/auth/query': 1,
			'/api/auth/cookie': 2,
			'/api/auth/header': 3,
			'/api/auth/http': 4,
			'/api/auth/oauth2/implicit': 5,
			'/api/auth/oauth2/implicit/token': 6,
			'/api/auth/oauth2/password': 7,
			'/api/auth/oauth2/password/token': 8,
			'/api/auth/oauth2/clientcredentials': 9,
			'/api/auth/oauth2/clientcredentials/token': 10,
			'/api/auth/oauth2/authorizationcode': 11,
			'/api/auth/oauth2/authorizationcode/token': 12,
		}.get(url, 99),
		sortMethod=lambda o: {
			'OPTIONS': 0,
			'POST': 1,
			'GET': 2,
			'PUT': 3,
			'DELETE': 4,
		}.get(o.upper(), 9),
	),
	url_prefix='/doc',
	title='Liquirizia.WSGI Sample API',
)

# add resources to router
aps.addFile('res/html/welcome.html', '/')
aps.addFile('res/favicon.ico', '/favicon.ico')
aps.addFiles('res/css', '/css')
aps.addFileSystemObject(
	FileSystemObjectHelper.Get('Sample'),
	prefix='/thumbs',
	onRequest=ToJPEG(),
)
aps.addFile('res/html/swagger.html', '/doc/swagger')
aps.addFile('res/html/redoc.html', '/doc/redoc')


if __name__ == '__main__':
	print('WSGI server init...')
	with serve('127.0.0.1', 8000, aps) as httpd:
		print('WSGI server run')
		httpd.serve_forever()
	print('WSGI server stopped')
