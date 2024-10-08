# -*- coding: utf-8 -*-

from .Documentation import Documentation

__all__ = (
	'Information',
	'Contact',
	'License',
)


class Contact(Documentation):
	def __init__(
		self,
		name: str = None,
		url: str = None,
		email: str = None,
	):
		super().__init__()
		if name: self.__document__['name'] = name
		if url: self.__document__['url'] = url
		if email: self.__document__['email'] = email
		return
	
class License(Documentation):
	def __init__(
		self,
		name: str,
		identifier: str = None,
		url: str = None,
	):
		super().__init__(
			name=name,
		)
		if identifier: self.__document__['identifier'] = identifier
		if url: self.__document__[url] = url
		return

class Information(Documentation):
	def __init__(
		self,
		title: str,
		version: str,
		summary: str = None,
		description: str = None,
		tos: str = None,
		contact: Contact = None,
		license: License = None,
	):
		super().__init__(
			title=title,
			version=version,
		)
		if summary: self.__document__['summary'] = summary
		if description: self.__document__['description'] = description
		if tos: self.__document__['termsOfService'] = tos
		if contact: self.__document__['contact'] = contact
		if license: self.__document__['license'] = license
		return
