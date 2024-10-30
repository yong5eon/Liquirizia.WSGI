# -*- coding: utf-8 -*-

from .Application import Application
from .Configuration import Configuration

from .Request import Request
from .Response import Response
from .RequestProperties import RequestProperties
from .RequestReader import RequestReader
from .ResponseWriter import ResponseWriter
from .Router import Router

from .Error import Error

from .Cookie import Cookie
from .CORS import CORS

from .RequestHandler import RequestHandler

from .Server import serve

from Liquirizia.Serializer import SerializerHelper
from .Serializers.FormUrlEncoded import (
	Encoder as FormUrlEncoder,
	Decoder as FormUrlDecoder,
	FORMATS as FORM_URL_ENCODED,
)

__all__ = (
	'Application',
	'Configuration',
	'Request',
	'Response',
	'RequestProperties',
	'RequestReader',
	'ResponseWriter',
	'Router',
	'Error',
	'Cookie',
	'CORS',
	'RequestHandler',
	'serve',
)

for FORMAT in FORM_URL_ENCODED:
	SerializerHelper.Set(FORMAT, FormUrlEncoder, FormUrlDecoder)
