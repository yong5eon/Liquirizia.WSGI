# -*- coding: utf-8 -*-
#
# Request Headers
# - Accept-Language # ACCEPT_LANGUAGE
# - Alt-Used # ALT_USED
# - Authorization # AUTHORIZATION
# - Cookie # COOKIE
# - Device-Memory # DEVICE_MEMORY
# - DNT # DNT
# - Downlink # DOWNLINK
# - DPR # DPR
# - Early-Data # EARLY_DATA
# - ECT # ECT
# - Expect # EXPECT
# - Forwarded # FORWARDED
# - From # FROM
# - Host # HOST
# - If-Match # IF_MATCH
# - If-Modified-Since # IF_MODIFIED_SINCE
# - If-Not-Match # IF_NOT_MATCH
# - If-Range # IF_RANGE
# - If-Unmodified-Since # IF_UNMODIFIED_SINCE
# - Max-Forwards # MAX_FORWARDS
# - Origin # ORIGIN
# - Proxy-Authorization # PROXY_AUTHORIZATION
# - Range # RANGE
# - Referer # REFERER
# - RTT # RTT
# - Save-Data # SAVE_DATA
# - Sec-Browsing-Topics # SEC_BROWSING_TOPICS
# - Sec-CH-Prefers-Color-Scheme # SEC_CH_PREFERS_COLOR_SCHEME
# - Sec-CH-Prefers-Reduced-Motion # SEC_CH_PREFERS_REDUCED_MOTION
# - Sec-CH-Prefers-Reduced-Transparency # SEC_CH_PREFERS_REDUCED_TRANSPARENCY
# - Sec-CH-UA # SEC_CH_UA
# - Sec-CH-UA-Arch # SEC_CH_UA_ARCH
# - Sec-CH-UA-Bitness # SEC_CH_UA_BITNESS
# - Sec-CH-UA-Full-Version # SEC_CH_UA_FULL_VERSION
# - Sec-CH-UA-Mobile # SEC_CH_UA_MOBILE
# - Sec-CH-UA-Model # SEC_CH_UA_MODEL
# - Sec-CH-UA-Platform # SEC_CH_UA_PLATFORM
# - Sec-CH-UA-Platform-Version # SEC_CH_UA_PLATFORM_VERSION
# - Sec-Fetch-Dest # SEC_FETCH_DEST
# - Sec-Fetch-Mode # SEC_FETCH_MODE
# - Sec-Fetch-Site # SEC_FETCH_SITE
# - Sec-Fetch-User # SEC_FETCH_USER
# - Sec-GPC # SEC_GPC
# - Sec-Purpose # SEC_PURPOSE
# - Service-Worker # SERVICE_WORKER
# - Service-Worker-Navigation-Prelaod # SERVICE_WORKER_NAVIGATION_PRELAOD
# - TE # TE
# - Upgrade-Insecure-Requests # UPGRADE_INSECURE_REQUESTS
# - User-Agent # USER_AGENT
# - Viewport-Width # VIEWPORT_WIDTH
# - Width # WIDTH
# - X-Forwarded-For # X_FORWARDED_FOR
# - X-Forwarded-Host # X_FORWARDED_HOST
# - X-Forwarded-Proto # X_FORWARDED_PROTO

from ..Header import (
	Header,
	HeaderAsList,
	HeaderAsParameter,
	HeaderAsParameters,
	HeaderWithParameters,
)

from datetime import datetime

__all__ = (
	'AcceptLanguage',
	'AltUsed',
	'Authorization',
	'DeviceMemory',
	'DNT',
	'Downlink',
	'DPR',
	'EarlyData',
	'ECT',
	'Forwarded',
	'IfMatch',
	'IfModifiedSince',
	'IfNoneMatch',
	'IfRange',
	'IfUnmodifiedSince',
)


class AcceptLanguage(HeaderAsList):
	def __init__(self, value: str):
		super().__init__(value, sep=',', format=HeaderWithParameters, options={'paramsep': ' '})
		for _ in self.__properties__:
			_.language = _.value
			if 'q' not in _.parameters.keys(): _.q = 1.0
			else: _.q = float(_.parameters['q'])
		self.__properties__ = sorted(self.__properties__, key=lambda x: x.q, reverse=True)
		return


class AltUsed(Header):
	def __init__(self, value):
		super().__init__(value)
		ts = value.strip().split(':', maxsplit=1)
		self.host = ts[0].strip().replace('"','').replace('<','').replace('>','')
		self.port = int(ts[1].strip().replace('"','').replace('<','').replace('>','')) if len(ts) > 1 else None
		return

class Authorization(Header):
	def __init__(self, value):
		super().__init__(value)
		ts = value.strip().split(' ', maxsplit=1)
		if ts[0].strip().lower() == 'digest':
			self.scheme = ts[0].strip()
			self.credentials = None
			self.parameters = {}
			for token in ts[1].strip().split(','):
				k, v = token.strip().split('=')
				self.parameters[k.strip().replace('"','').replace('<','').replace('>','')] = v.strip().replace('"','').replace('<','').replace('>','')
		else:
			self.scheme = ts[0].strip()
			self.credentials = ts[1].strip().replace('"','').replace('<','').replace('>','')
			self.parameters = {}
		return


class DeviceMemory(Header):
	def __init__(self, value):
		super().__init__(value)
		return


class DNT(Header):
	def __init__(self, value):
		super().__init__(value)
		return


class Downlink(Header):
	def __init__(self, value):
		super().__init__(value)
		return


class DPR(Header):
	def __init__(self, value):
		super().__init__(value)
		return


class EarlyData(Header):
	def __init__(self, value):
		super().__init__(value)
		return


class ECT(Header):
	def __init__(self, value):
		super().__init__(value)
		return


class Forwarded(HeaderAsParameters):
	def __init__(self, value):
		super().__init__(value, sep=';')
		return


class From(Header):
	def __init__(self, value):
		super().__init__(value)
		return


class Host(Header):
	def __init__(self, value):
		super().__init__(value)
		return


class IfMatch(HeaderAsList):
	def __init__(self, value):
		super().__init__(value, sep=',')
		for _ in self.__properties__:
			_.__val__ = _.__val__.strip().replace('"','').replace('<','').replace('>','')
		return
	

class IfModifiedSince(Header):
	def __init__(self, value: str):
		super().__init__(value)
		try:
			self.datetime = datetime.strptime(value, '%a, %d %b %Y %H:%M:%S GMT')
		except:
			self.datetime = None
		return


class IfNoneMatch(HeaderAsList):
	def __init__(self, value):
		super().__init__(value, sep=',')
		for _ in self.__properties__:
			_.__val__ = _.__val__.strip().replace('"','').replace('<','').replace('>','')
		return

class IfRange(Header):
	def __init__(self, value: str):
		super().__init__(value)
		try:
			self.datetime = datetime.strptime(value, '%a, %d %b %Y %H:%M:%S GMT')
			self.etag = None
		except:
			self.datetime = None
			self.etag = value.strip().replace('"','')
		return


class IfUnmodifiedSince(Header):
	def __init__(self, value: str):
		super().__init__(value)
		try:
			self.datetime = datetime.strptime(value, '%a, %d %b %Y %H:%M:%S GMT')
		except:
			self.datetime = None
		return

