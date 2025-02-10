# -*- coding: utf-8 -*-

from Liquirizia.WSGI import (
		Application, 
		Configuration,
		Handler,
		Request,
		Response,
		Router,
		Error,
		serve,
)
from Liquirizia.WSGI.Responses import *
from Liquirizia.WSGI.Filters import RequestFilters
from Liquirizia.WSGI.Documentation import Information, Contact

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
	FileSystemObjectConfiguration('sample/res/images')
)

class SampleHandler(Handler):
	def onRequest(self, request: Request):
		print('{} - {} - REQUEST BEGIN     - {}'.format(datetime.now().isoformat(), request.id[:16], str(request)))
		return request, None
	def onRequestResponse(self, request: Request, response: Response):
		print('{} - {} - REQUEST RESPONSE  - {} - {}'.format(datetime.now().isoformat(), request.id[:16], str(response), response.size))
		return response
	def onRequestComplete(self, request: Request):
		print('{} - {} - REQUEST DONE      - {}'.format(datetime.now().isoformat(), request.id[:16], str(request)))
		return
	def onRequestError(self, request: Request, error: Error):
		print('{} - {} - REQUEST ERROR     - {}'.format(datetime.now().isoformat(), request.id[:16], str(request)))
		print(error.traceback)
		return ResponseError(error)
	def onRequestException(self, request: Request, e: Exception):
		print('{} - {} - REQUEST EXCEPTION - {}'.format(datetime.now().isoformat(), request.id[:16], str(request)))
		tb =	str(e)
		tb += '\n'
		tb += ''.join(format_tb(e.__traceback__)).strip().replace(' ' * 4, ' ' * 2)
		print(tb)
		return ResponseInternalServerError(body=tb, format='text/plain', charset='utf-8')
	def onError(self, env, error: Error):
		print('{} - {} - ERROR            - {} - {}'.format(datetime.now().isoformat(), env['REQUEST_ID'][:16], env['PATH_INFO'], str(error)))
		print(error.traceback)
		return ResponseError(error)
	def onException(self, env, e: Exception):
		print('{} - {} - EXCEPTION        - {} - {}'.format(datetime.now().isoformat(), env['REQUEST_ID'][:16], env['PATH_INFO'], str(e)))
		tb =	str(e)
		tb += '\n'
		tb += ''.join(format_tb(e.__traceback__)).strip().replace(' ' * 4, ' ' * 2)
		print(tb)
		return ResponseServiceUnavailable(body=tb, format='text/plain', charset='utf-8')


aps = Application(
	handler=SampleHandler(),
	conf=Configuration(
		headers={
			'X_TOKEN': 'X-Token',
		},
	)
)

aps.load(path='sample/api')

# apply swagger-ui
import sys
import DocumentHandler

from swagger_ui import supported_list

sys.modules['swagger_ui.handlers.Liquirizia'] = DocumentHandler
supported_list.append('Liquirizia')

from Liquirizia.WSGI import Application, Configuration, Router
from Liquirizia.WSGI.Documentation import (
	Information,
	Contact,
)
from swagger_ui import api_doc

api_doc(
	aps,
	config=Router().toDocument(
		info=Information(
			title='Liquirizia.WSGI Sample API',
			version='0.1.0',
			summary='Sample API Document',
			description='Sample API',
			contact=Contact(
				name='Heo Yongseon',
				url='https://github.com/yong5eon/Liquirizia.WSGI',
				email='contact@email.com'
			)
		)
	),
	url_prefix='/doc',
	title='Liquirizia.WSGI Sample API',
)

# add resources to router
aps.addFile('sample/res/html/welcome.html', '/')
aps.addFile('sample/res/favicon.ico', '/favicon.ico')
aps.addFiles('sample/res/css', '/css')
aps.addFileSystemObject(
	FileSystemObjectHelper.Get('Sample'),
	prefix='/thumbs',
	onRequest=RequestFilters(ToJPEG()),
)


if __name__ == '__main__':
	print('WSGI server init...')
	with serve('127.0.0.1', 8000, aps) as httpd:
		print('WSGI server run')
		httpd.serve_forever()
	print('WSGI server stopped')
