# -*- coding: utf-8 -*-

from ..Error import Error

from typing import Dict, Any

__all__ = (
	'InternalServerError', # 500
	'NotImplementedError', # 501
	'ServiceUnavailableError', # 503
	'VersionNotSupportedError', # 505
	'NotExtendedError', # 510
	'NetworkAuthenticationRequiredError', # 511
)


class InternalServerError(Error):
	"""Internal Server Error Class, 500"""
	def __init__(
		self,
		reason: str,
		headers: Dict[str, Any] = None,
		body: bytes = None,
		format: str = None,
		charset: str = None,
		error: BaseException = None,
	):
		super(InternalServerError, self).__init__(
			reason,
			500,
			'Internal Server Error',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
			error=error,
		)
		return


class NotImplementedError(Error):
	"""Not Implemented Error Class, 501"""
	def __init__(
		self,
		reason: str,
		headers: Dict[str, Any] = None,
		body: bytes = None,
		format: str = None,
		charset: str = None,
		error: BaseException = None,
	):
		super(NotImplementedError, self).__init__(
			reason,
			501,
			'Not Implemented',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
			error=error,
		)
		return


class ServiceUnavailableError(Error):
	"""Service Unavailable Error Class, 503"""
	def __init__(
		self,
		reason: str,
		headers: Dict[str, Any] = None,
		body: bytes = None,
		format: str = None,
		charset: str = None,
		error: BaseException = None,
	):
		super(ServiceUnavailableError, self).__init__(
			reason,
			503,
			'Service Unavailable',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
			error=error,
		)
		return


class VersionNotSupportedError(Error):
	"""HTTP Version Not Supported Error Class, 505"""
	def __init__(
		self,
		reason: str,
		headers: Dict[str, Any] = None,
		body: bytes = None,
		format: str = None,
		charset: str = None,
		error: BaseException = None,
	):
		super(VersionNotSupportedError, self).__init__(
			reason,
			505,
			'Version Not Supported',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
			error=error,
		)
		return


class NotExtendedError(Error):
	"""NotExtended Error Class, 510"""
	def __init__(
		self,
		reason: str,
		headers: Dict[str, Any] = None,
		body: bytes = None,
		format: str = None,
		charset: str = None,
		error: BaseException = None,
	):
		super(NotExtendedError, self).__init__(
			reason,
			510,
			'Not Extended',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
			error=error,
		)
		return


class NetworkAuthenticationRequiredError(Error):
	"""Network Authentication Required Error Class, 511"""
	def __init__(
		self,
		reason: str,
		headers: Dict[str, Any] = None,
		body: bytes = None,
		format: str = None,
		charset: str = None,
		error: BaseException = None,
	):
		super(NetworkAuthenticationRequiredError, self).__init__(
			reason,
			511,
			'Network Authentication Required',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
			error=error,
		)
		return
