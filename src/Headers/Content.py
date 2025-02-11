# -*- coding: utf-8 -*-
#
# Content Headers
# - Content-Digest # CONTENT_DIGEST
# - Content-Disposision # CONTENT_DISPOSISION
# - Content-DPR # CONTENT_DPR
# - Content-Encoding # CONTENT_ENCODING
# - Content-Language # CONTENT_LANGUAGE
# - Content-Length # CONTENT_LENGTH
# - Content-Location # CONTENT_LOCATION
# - Content-Range # CONTENT_RANGE
# - Content-Security-Policy # CONTENT_SECURITY_POLICY
# - Content-Security-Policy-Report-Only # CONTENT_SECURITY_POLICY_REPORT_ONLY
# - Content-Type # CONTENT_TYPE
# - ETag # ETAG
# - Last-Modified # LAST_MODIFIED
# - Repr-Digest # REPR_DIGEST
# - Trailer # TRAILER
# - Transfer-Encoding # TRANSFER_ENCODING
# - Want-Content-Digest # WANT_CONTENT_DIGEST
# - Want-Repr-Digest # WANT_REPR_DIGEST

from ..Header import (
	Header,
	HeaderAsList,
	HeaderAsParameter,
	HeaderAsParameters,
	HeaderWithParameters,
)

from datetime import datetime

__all__ = (
	'ContentDigest',
	'ContentDisposition',
	'ContentDPR',
	'ContentEncoding',
	'ContentLanguage',
	'ContentLength',
	'ContentLocation',
	'ContentRange',
	'ContentSecuriyPolicy',
	'ContentSecuriyPolicyReportOnly',
	'ContentType'
	'ETag',
	'LastModified',
	'ReprDigest',
	'Trailer',
	'TransferEncoding',
	'WantContentDigest',
	'WantReprDigest',
)


class ContentDigest(HeaderAsParameters):
	def __init__(self, value):
		super().__init__(value, sep=',')
		return
	

class ContentDisposition(HeaderWithParameters):
	def __init__(self, value):
		super().__init__(value, sep=';', paramsep=';')
		return


class ContentDPR(Header):
	def __init__(self, value):
		super().__init__(value)
		return


class ContentEncoding(HeaderAsList):
	def __init__(self, value):
		super().__init__(value, sep=',')
		return


class ContentLanguage(HeaderAsList):
	def __init__(self, value):
		super().__init__(value, sep=',')
		return


class ContentLength(Header):
	def __init__(self, value):
		super().__init__(value)
		return


class ContentLocation(Header):
	def __init__(self, value):
		super().__init__(value)
		return


class ContentRange(Header):
	def __init__(self, value):
		super().__init__(value)
		ts = value.strip().split(' ', maxsplit=1)
		self.unit = ts[0].strip().replace('"','').replace('<','').replace('>','')
		rs = ts[1].strip().split('/')
		self.size = int(rs[1].strip()) if rs[1].strip() != '*' else None
		if rs[0].strip() == '*':
			self.offset = 0
			self.end = None
		else:
			ss = rs[0].strip().split('-')
			self.offset = int(ss[0].strip())
			self.end = int(ss[1].strip())
		return


class ContentSecurityPolicy(HeaderAsList):
	def __init__(self, value):
		super().__init__(value, sep=';')
		return


class ContentSecurityPolicyReportOnly(HeaderAsList):
	def __init__(self, value):
		super().__init__(value, sep=';')
		return
	

class ContentType(HeaderWithParameters):
	def __init__(self, value, sep = ';', paramsep = ','):
		super().__init__(value, sep, paramsep)
		self.charset = self.parameters['charset'] if 'charset' in self.parameters else None
		self.boundary= self.parameters['boundary'] if 'boundary' in self.parameters else None
		return


class ETag(Header):
	def __init__(self, value):
		super().__init__(value)
		if value[:2] == 'W/': value = value[2:]
		self.etag = value.strip().replace('"',"").replace('<','').replace('>','')
		return


class LastModified(Header):
	def __init__(self, value: str):
		super().__init__(value)
		try:
			self.__datetime__ = datetime.strptime(value, '%a, %d %b %Y %H:%M:%S GMT')
		except:
			self.__datetime__ = None
		return
	@property
	def dt(self): self.__datetime__


class ReprDigest(HeaderAsParameters):
	def __init__(self, value):
		super().__init__(value, sep=',')
		return
	

class Trailer(Header):
	def __init__(self, value):
		super().__init__(value)
		return
	

class TransferEncoding(HeaderAsList):
	def __init__(self, value):
		super().__init__(value, sep=',')
		return


class WantContentDigest(HeaderAsParameters):
	def __init__(self, value):
		super().__init__(value, sep=',')
		return


class WantReprDigest(HeaderAsParameters):
	def __init__(self, value):
		super().__init__(value, sep=',')
		return


