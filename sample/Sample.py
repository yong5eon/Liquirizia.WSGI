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


from filters import ToJPEG
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
		'X_TOKEN': 'X-Token',
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

Load(mod='api')

from api.Format import *
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
			Tag('RequestRunner - Content Validation', description='일반적인 요청 처리 시 본문으로 전달되는 컨텐츠의 유효성 검사 예제'),
			Tag('RequestStreamRunner', description='스트림 요청 처리 예제'),
			Tag('RequestStreamRunner - Chunked', description='청크 스트림 요청 처리 예제'),
			Tag('RequestServerSentEventsRunner', description='Server-Sent Events 요청 처리 예제'),
			Tag('RequestWebSocketRunner', description='WebSocket 요청 처리 예제'),
		),
		schemas=(
			FormatError,
			FormatRequest,
			FormatResponse,	
			FormatData,
			FormatParameters,
			FormatQueryString,
			FormatContent,
			FormatExtra,
		),
		url=lambda url: {
			'/api/content/bool': '11',
			'/api/content/integer': '12',
			'/api/content/number': '13',
			'/api/content/string': '14',
			'/api/content/array': '14',
			'/api/content/object': '14',
		}.get(url, '99'),
		method=lambda o: {
			'GET': 1,
			'POST': 2,
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
