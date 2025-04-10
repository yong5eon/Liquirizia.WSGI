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
from Liquirizia.WSGI.Filters import RequestFilters
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
		print('{} - {} - REQUEST BEGIN     - {} - {} - {} - {}'.format(
			datetime.now().isoformat(),
			request.id[:16],
			request.remote,
			str(request),
			request.header('Content-Type'),
			request.size,
		))
		print('Protocol - {}'.format(request.protocol if request.protocol else None))
		print('Platform - {}'.format(request.platform.upper() if request.platform else None))
		print('Device - {}'.format(request.device.upper() if request.device else None))
		print('Is-Mobile - {}'.format(request.isMobile))
		for k, _ in request.headers():
			print('{} - {}'.format(k, request.header(k)))
		return request, None
	def onRequestResponse(self, request: Request, response: Response):
		print('{} - {} - REQUEST RESPONSE  - {} - {} - {}'.format(
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
		print('{} - {} - REQUEST DONE      - {} - {}'.format(
			datetime.now().isoformat(),
			request.id[:16],
			request.remote,
			str(request)
		))
		return
	def onRequestError(self, request: Request, error: Error):
		print('{} - {} - REQUEST ERROR     - {} - {}'.format(
			datetime.now().isoformat(),
			request.id[:16],
			request.remote,
			str(request)
		))
		print(error.traceback)
		return ResponseError(error)
	def onRequestException(self, request: Request, e: Exception):
		print('{} - {} - REQUEST EXCEPTION - {} - {}'.format(
			datetime.now().isoformat(),
			request.id[:16],
			request.remote,
			str(request)
		))
		tb =	str(e)
		tb += '\n'
		tb += ''.join(format_tb(e.__traceback__)).strip().replace(' ' * 4, ' ' * 2)
		print(tb)
		return ResponseInternalServerError(body=tb.encode(), format='text/plain', charset='utf-8')
	def onError(self, env, error: Error):
		print('{} - {} - ERROR            - {} - {}'.format(
			datetime.now().isoformat(),
			env['REQUEST_ID'][:16],
			env['PATH_INFO'],
			str(error)
		))
		print(error.traceback)
		return ResponseError(error)
	def onException(self, env, e: Exception):
		print('{} - {} - EXCEPTION        - {} - {}'.format(
			datetime.now().isoformat(),
			env['REQUEST_ID'][:16],
			env['PATH_INFO'],
			str(e)
		))
		tb =	str(e)
		tb += '\n'
		tb += ''.join(format_tb(e.__traceback__)).strip().replace(' ' * 4, ' ' * 2)
		print(tb)
		return ResponseServiceUnavailable(body=tb.encode(), format='text/plain', charset='utf-8')


aps = Application(
	handler=SampleHandler(),
	headers={
		'X_APP_ID': 'X-App-Id',
		'CREDENTIALS': 'Credentials',
	},
)

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
	# version='3.0.0'
)

Load(mod='runners')

# import model
from Liquirizia.Description import ToSchema
from runners.Model import *
# apply swagger-ui
import sys
import DocumentHandler

from swagger_ui import supported_list

sys.modules['swagger_ui.handlers.Liquirizia'] = DocumentHandler
supported_list.append('Liquirizia')

from swagger_ui import api_doc

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
			ToSchema(ParametersModel),
			ToSchema(QueriesModel),
			ToSchema(ContentModel),
			ToSchema(ArgumentsModel),
			ToSchema(DataModel),
			ToSchema(ResponseModel),
		),
		sortUrl=lambda url: {
			# content validation
			'/api/content/bool': 1,
			'/api/content/integer': 2,
			'/api/content/number': 3,
			'/api/content/string': 4,
			'/api/content/array': 5,
			'/api/content/object': 6,
			# auth
			'/api/auth/http': 1,
			'/api/auth/header': 2,
			'/api/auth/cookie': 3,
			'/api/auth/query': 4,
		}.get(url, 99),
		sortMethod=lambda o: {
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
	onRequest=RequestFilters(ToJPEG()),
)
aps.addFile('res/html/swagger.html', '/doc/swagger')
aps.addFile('res/html/redoc.html', '/doc/redoc')


if __name__ == '__main__':
	print('WSGI server init...')
	with serve('127.0.0.1', 8000, aps) as httpd:
		print('WSGI server run')
		httpd.serve_forever()
	print('WSGI server stopped')
