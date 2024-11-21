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

PATH = dirname(realpath(__file__))

FileSystemObjectHelper.Set(
		'Sample',
		FileSystemObject,
		FileSystemObjectConfiguration('sample/res/images')
)

class SampleHandler(Handler):
		def onRequest(self, request: Request):
				print('REQUEST	: {}'.format(str(request)))
				return request, None
		def onRequestResponse(self, request: Request, response: Response):
				print('REQUEST RESPONSE : {} - {}'.format(str(response), response.size))
				return response
		def onRequestComplete(self, request: Request):
				print('REQUEST COMPLETE : {}'.format(str(request)))
				return
		def onRequestError(self, request: Request, error: Error):
				print('REQUEST ERROR : {}'.format(str(request)))
				tb =	str(error)
				tb += '\n'
				for line in ''.join(format_tb(error.__traceback__)).strip().split('\n'):
						tb += line
						tb += '\n'
				print(tb)
				return ResponseError(error, body=tb, format='text/plain', charset='utf-8')
		def onRequestException(self, request: Request, e: Exception):
				print('REQUEST EXCEPTION : {}'.format(str(request)))
				tb =	str(e)
				tb += '\n'
				for line in ''.join(format_tb(e.__traceback__)).strip().split('\n'):
						tb += line
						tb += '\n'
				print(tb)
				return ResponseInternalServerError(body=tb, format='text/plain', charset='utf-8')
		def onError(self, error: Error):
				print('ERROR : {}'.format(str(error)))
				tb =	str(error)
				tb += '\n'
				for line in ''.join(format_tb(error.__traceback__)).strip().split('\n'):
						tb += line
						tb += '\n'
				print(tb)
				return ResponseError(error, body=tb, format='text/plain', charset='utf-8')
		def onException(self, e: Exception):
				print('EXCEPTION : {}'.format(str(e)))
				tb =	str(e)
				tb += '\n'
				for line in ''.join(format_tb(e.__traceback__)).strip().split('\n'):
						tb += line
						tb += '\n'
				print(tb)
				return ResponseServiceUnavailable(body=tb, format='text/plain', charset='utf-8')


aps = Application(
		handler=SampleHandler(),
		conf=Configuration(
				envToHeaders={
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
	with serve('127.0.0.1', 8000, aps) as httpd:
		httpd.serve_forever()
