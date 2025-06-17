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
		headers: Dict[str, Any] = None,
		body: bytes = None,
		format: str = None,
		charset: str = None,
		reason: str = None,
		error: BaseException = None,
		extra: Any = None,
	):
		super(InternalServerError, self).__init__(
			500,
			'Internal Server Error',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
			reason=reason,
			error=error,
			extra=extra,
		)
		return


class NotImplementedError(Error):
	"""Not Implemented Error Class, 501"""
	def __init__(
		self,
		headers: Dict[str, Any] = None,
		body: bytes = None,
		format: str = None,
		charset: str = None,
		reason: str = None,
		error: BaseException = None,
		extra: Any = None,
	):
		super(NotImplementedError, self).__init__(
			501,
			'Not Implemented',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
			reason=reason,
			error=error,
			extra=extra,
		)
		return


class ServiceUnavailableError(Error):
	"""Service Unavailable Error Class, 503"""
	def __init__(
		self,
		headers: Dict[str, Any] = None,
		body: bytes = None,
		format: str = None,
		charset: str = None,
		reason: str = None,
		error: BaseException = None,
		extra: Any = None,
	):
		super(ServiceUnavailableError, self).__init__(
			503,
			'Service Unavailable',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
			reason=reason,
			error=error,
			extra=extra,
		)
		return


class VersionNotSupportedError(Error):
	"""HTTP Version Not Supported Error Class, 505"""
	def __init__(
		self,
		headers: Dict[str, Any] = None,
		body: bytes = None,
		format: str = None,
		charset: str = None,
		reason: str = None,
		error: BaseException = None,
		extra: Any = None,
	):
		super(VersionNotSupportedError, self).__init__(
			505,
			'Version Not Supported',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
			reason=reason,
			error=error,
			extra=extra,
		)
		return


class NotExtendedError(Error):
	"""NotExtended Error Class, 510"""
	def __init__(
		self,
		headers: Dict[str, Any] = None,
		body: bytes = None,
		format: str = None,
		charset: str = None,
		reason: str = None,
		error: BaseException = None,
		extra: Any = None,
	):
		super(NotExtendedError, self).__init__(
			510,
			'Not Extended',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
			reason=reason,
			error=error,
			extra=extra,
		)
		return


class NetworkAuthenticationRequiredError(Error):
	"""Network Authentication Required Error Class, 511"""
	def __init__(
		self,
		headers: Dict[str, Any] = None,
		body: bytes = None,
		format: str = None,
		charset: str = None,
		reason: str = None,
		error: BaseException = None,
		extra: Any = None,
	):
		super(NetworkAuthenticationRequiredError, self).__init__(
			511,
			'Network Authentication Required',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
			reason=reason,
			error=error,
			extra=extra,
		)
		return
