# -*- coding: utf-8 -*-
#
# Common Headers
# - Accept # ACCEPT
# - Accept-Encoding # ACCEPT_ENCODING
# - Cache-Control # CACHE_CONTROL
# - Connection # CONNECTION
# - Date # DATE
# - Keep-Alive # KEEP_ALIVE
# - Link # LINK
# - Pragma # PRAGMA
# - Priority # PRIORITY
# - Upgrade # UPGRADE
# - Via # VIA
# - Warning # WARNING

from ..Header import (
	Header,
	HeaderWithParameters,
	HeaderAsParameter,
	HeaderAsParameters,
	HeaderAsList,
)

from ..Util import ToDatetime

__all__ = (
	'Accept',
	'AcceptEncoding',
	'CacheControl',
	'Connection',
	'Date',
	'KeepAlive',
	'Link',
	'Pragma',
	'Priority',
	'Upgrade',
	'Via',
	'Warning',
)

class Accept(HeaderAsList):
	def __init__(self, value: str):
		super().__init__(value, sep=',', format=HeaderWithParameters, options={'paramsep': ' '})
		for _ in self.__properties__:
			_.mimetype, _.subtype = _.value.split('/')
			if 'q' not in _.parameters.keys(): _.q = 1.0
			else: _.q = float(_.parameters['q'])
		self.__properties__ = sorted(self.__properties__, key=lambda x: x.q, reverse=True)
		return


class AcceptEncoding(HeaderAsList):
	def __init__(self, value: str):
		super().__init__(value, sep=',', format=HeaderWithParameters, options={'paramsep': ' '})
		for _ in self.__properties__:
			_.directive = _.value
			if 'q' not in _.parameters.keys(): _.q = 1.0
			else: _.q = float(_.parameters['q'])
		self.__properties__ = sorted(self.__properties__, key=lambda x: x.q, reverse=True)
		return
	

class CacheControl(HeaderAsList):
	def __init__(self, value: str):
		super().__init__(value, sep=',', format=HeaderAsParameter)
		for _ in self.__properties__:
			_.directive = _.key
			_.seconds = int(_.weight) if _.weight else _.weight
		return
	

class Connection(Header):
	def __init__(self, value: str):
		super().__init__(value)
		return


class Date(Header):
	def __init__(self, value: str):
		super().__init__(value)
		try:
			self.__datetime__ = ToDatetime(value)
		except:
			self.__datetime__ = None
		return
	@property
	def dt(self): self.__datetime__


class KeepAlive(HeaderAsParameters):
	def __init__(self, value: str):
		super().__init__(value, sep=',')
		return
	

class Link(HeaderAsList):
	def __init__(self, value):
		super().__init__(value, sep=',', format=HeaderWithParameters, options={'sep':';', 'paramsep':';'})
		for _ in self.__properties__:
			_.reference = _.value
		return


class Pragma(Header):
	def __init__(self, value: str):
		super().__init__(value)
		return


class Priority(HeaderAsParameters):
	def __init__(self, value):
		super().__init__(value, sep=',')
		self.u = self.__properties__['u'] if 'u' in self.__properties__.keys() else None
		self.i = True if 'i' in self.__properties__.keys() else False
		return


class Upgrade(HeaderAsList):
	def __init__(self, value):
		super().__init__(value, sep=',', format=Header)
		for _ in self.__properties__:
			ts = str(_).strip().split('/')
			_.protocol = ts[0].strip().replace('"','').replace('<','').replace('>','')
			_.version = ts[1].strip().replace('"','').replace('<','').replace('>','') if len(ts) > 1 else None
		return
	

class Via(HeaderAsList):
	def __init__(self, value):
		super().__init__(value, sep=',', format=Header)
		for _ in self.__properties__:
			ts = str(_).strip().split(' ')
			_.protocolVersion = ts[0].strip().replace('"','').replace('<','').replace('>','')
			_.protocol = None
			_.version = _.protocolVersion
			ptvs = _.protocolVersion.split('/')
			if len(ptvs) > 1:
				_.protocol = ptvs[0]
				_.version = ptvs[1]
			_.host = ts[1].strip().replace('"','').replace('<','').replace('>','')
			_.port = None
			addrs = _.host.split(':')
			if len(addrs) > 1:
				_.host = addrs[0]
				_.port = addrs[1]
		return


class Warning(Header):
	def __init__(self, value):
		super().__init__(value)
		# TODO: 
		return
