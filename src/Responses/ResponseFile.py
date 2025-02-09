# -*- coding: utf-8 -*-

from ..Response import Response

from ..Errors import RangeNotSatisfiableError

from mimetypes import guess_type
from os import stat
from os.path import isfile, split

from email.utils import formatdate
from hashlib import sha1

from typing import Dict, Any

__all__ = (
	'ResponseFile'
)


class ResponseFile(Response):
	"""Response File Class"""

	def __init__(
		self,
		file,
		offset=None,
		size=None,
		status=200,
		message='OK',
		headers: Dict[str, Any] = {} 
	):
		super(ResponseFile, self).__init__(status=status, message=message, headers=headers)

		if not isfile(file):
			raise IOError('Resource {} is not found'.format(file))

		head, tail = split(file)
		stats = stat(file)

		fmt, charset = guess_type(file)
		super(ResponseFile, self).header('Content-Type', '{}{}'.format(fmt, '; charset={}'.format(charset) if charset else ''))
		if charset:
			super(ResponseFile, self).header('Content-Encoding', charset)
		super(ResponseFile, self).header('Last-Modified', formatdate(stats.st_mtime, usegmt=True))
		etag = '{}:{}:{}:{}:{}'.format(stats.st_dev, stats.st_ino, stats.st_mtime, stats.st_size, tail)
		super(ResponseFile, self).header('ETag', sha1(etag.encode('utf-8')).hexdigest())

		with open(file, 'rb') as f:
			if offset:
				if size:
					if offset + size > stats.st_size:
						raise RangeNotSatisfiableError('Illegal Ranges')
					self.range(offset, offset + size, size)
				else:
					self.range(offset, stats.st_size, stats.st_size - offset)
				f.seek(offset)
			else:
				super(ResponseFile, self).header('Content-Length', str(stats.st_size))
			self.body = f.read(self.size)
			f.close()
		return

	def range(self, offset, end, size):
		super(ResponseFile, self).status = 206
		super(ResponseFile, self).message = 'Partial Content'
		super(ResponseFile, self).header('Content-Range', 'bytes {}-{}/{}'.format(offset, end - 1, size))
		super(ResponseFile, self).header('Content-Length', str(end - offset))
		return
