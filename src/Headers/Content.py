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

__all__ = (
	'ContentDigest',
	'ContentDisposition',
	'ContentDPR',
	'ContentEncoding',
	'ContentLanguage',
	'ContentLength',
	'ReprContentDigest',
	'WantContentDigest',
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


class ReprContentDigest(HeaderAsParameters):
	def __init__(self, value):
		super().__init__(value, sep=',')
		return


class WantContentDigest(HeaderAsParameters):
	def __init__(self, value):
		super().__init__(value, sep=',')
		return


