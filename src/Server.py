# -*- coding: utf-8 -*-

from wsgiref.simple_server import (
	make_server,
	WSGIServer,
	WSGIRequestHandler,
)
from wsgiref.handlers import SimpleHandler, BaseHandler

__all__ = (
	'serve'
)

class Server(WSGIServer): pass

class ServerHandler(BaseHandler):
	server_software = 'Liquirizia(WSGI)'
	def __init__(
		self,
		stdin,
		stdout,
		stderr,
		environ,
		multithread=True,
		multiprocess=False,
	):
		self.stdin = stdin
		self.stdout = stdout
		self.stderr = stderr
		self.base_env = environ
		self.wsgi_multithread = multithread
		self.wsgi_multiprocess = multiprocess

	def get_stdin(self):
		return self.stdin

	def get_stderr(self):
		return self.stderr

	def add_cgi_vars(self):
		self.environ.update(self.base_env)

	def _write(self,data):
		result = self.stdout.write(data)
		if result is None or result == len(data):
			return
		while True:
			data = data[result:]
			if not data:
				break
			result = self.stdout.write(data)

	def _flush(self):
		self.stdout.flush()
		self._flush = self.stdout.flush

	def close(self):
		SimpleHandler.close(self)
		return

	def send_headers(self):
		self.cleanup_headers()
		self.headers_sent = True
		if not self.origin_server or self.client_is_modern():
			self.send_preamble()
			self._write(bytes(self.headers))
			self._flush()
		return

	def start_response(self, status, headers, exc_info=None):
		if exc_info:
			try:
				if self.headers_sent:
					raise
			finally:
				exc_info = None		# avoid dangling circular ref
		elif self.headers is not None:
			raise AssertionError("Headers already set!")
		
		self.status = status
		self.headers = self.headers_class(headers)
		status = self._convert_string_type(status, "Status")
		assert len(status)>=4,"Status must be at least 4 characters"
		assert status[:3].isdigit(), "Status message must begin w/3-digit code"
		assert status[3]==" ", "Status message must have a space after code"
		self.send_headers()
		return self.write
	
	def finish_response(self):
		try:
			if not self.result_is_file() or not self.sendfile():
				for data in self.result if self.result else []:
					self.write(data)
				self.finish_content()
		except:
			# Call close() on the iterable returned by the WSGI application
			# in case of an exception.
			if hasattr(self.result, 'close'):
				self.result.close()
			raise
		else:
			# We only call close() when no exception is raised, because it
			# will set status, result, headers, and environ fields to None.
			# See bpo-29183 for more details.
			self.close()
		return


class ServerRequestHandler(WSGIRequestHandler):
	def handle(self):
		self.raw_requestline = self.rfile.readline(65537)
		if len(self.raw_requestline) > 65536:
			self.requestline = ''
			self.request_version = ''
			self.command = ''
			self.send_error(414)
			return

		if not self.parse_request(): # An error code has been sent, just exit
			return

		handler = ServerHandler(
			self.rfile,
			self.wfile,
			self.get_stderr(),
			self.get_environ(),
			multithread=True,
			multiprocess=False,
		)
		handler.request_handler = self	  # backpointer for logging
		handler.run(self.server.get_app())
		return


def serve(host, port, app):
	"""Create a new WSGI server listening on `host` and `port` for `app`"""
	server = Server((host, port), ServerRequestHandler)
	server.set_app(app)
	return server
