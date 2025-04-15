# -*- coding: utf-8 -*-

from Liquirizia.FileSystemObject import Helper as FileSystemObjectHelper
from Liquirizia.FileSystemObject.Implements.FileSystem import (
		Configuration as FileSystemObjectConfiguration, 
		Connection as FileSystemObject,
)
from Liquirizia.WSGI.Properties import RequestRunner
from Liquirizia.WSGI.Request import Request
from Liquirizia.WSGI import Response

from swagger_ui.core import ApplicationDocument

from collections.abc import Mapping
from json import dumps

def handler(doc: ApplicationDocument):

		class GetAPIDocument(RequestRunner):
				def __init__(self, request: Request):
						self.request = request
						return
				def run(self):
						return Response(
								status=200,
								message='OK',
								body=doc.doc_html.encode('utf-8'),
								format='text/html',
								charset='utf-8',
						)
		doc.app.add(
				object=GetAPIDocument,
				method='GET',
				url=doc.url_prefix,
		)

		class GetAPIConfig(RequestRunner):
				def __init__(self, request: Request):
						self.request = request
						return
				def run(self):
						def encoder(o):
								if isinstance(o, Mapping): return dict(o)
								raise TypeError(
										'Object of type {} is not JSON serializable'.format(type(o).__name__)
								)
						return Response(
								status=200,
								message='OK',
								body=dumps(
										doc.get_config(self.request.header('Host')),
										default=encoder
								).encode('utf-8'), 
								format='application/json',
								charset='utf-8',
						)
		doc.app.add(object=GetAPIConfig, method='GET', url=doc.swagger_json_uri_absolute)
		FileSystemObjectHelper.Set(
				'DocumentResource',
				FileSystemObject,
				FileSystemObjectConfiguration(doc.static_dir)
		)
		doc.app.addFileSystemObject(
				FileSystemObjectHelper.Get('DocumentResource'),
				doc.static_uri_absolute, 
		)
		return

def match(doc: ApplicationDocument):
		try:
				from Liquirizia.WSGI import Application
				if isinstance(doc.app, Application):
						return handler
		except ImportError:
				pass
		return None
