# -*- coding: utf-8 -*-

from Liquirizia.Test import *
from Liquirizia.WSGI.Utils import ParseRequestHeader

from datetime import datetime


class TestParseRequestHeader(Case):
	# Common Headers
	# - ACCEPT : ParseAccept()
	# - ACCEPT_ENCODING : ParseAcceptEncoding()
	# - CACHE_CONTROL : ParseCacheControl()
	# - CONNECTION : ParseString()
	# - DATE : ParseDate()
	# - KEEP_ALIVE : ParseParameters()
	# - LINK : ParseLink()
	# - PRAGMA : ParseString()
	# - PRIORITY : ParsePriority()
	# - UPGRADE : ParseUpgrade()
	# - VIA : ParseVia()
	# - WARNING : ParseString()
	@Parameterized(
		{
			'i': 'application/json, application/x-www-form-urlencoded; q=0.6, application/xml; q=0.7',
			'o': [
				{'type': 'application/json', 'q': 1.0, 'mimetype': 'application', 'subtype': 'json'},
				{'type': 'application/xml', 'q': 0.7, 'mimetype': 'application', 'subtype': 'xml'},
				{'type': 'application/x-www-form-urlencoded', 'q': 0.6, 'mimetype': 'application', 'subtype': 'x-www-form-urlencoded'},
			]
		},
	)
	@Order(101)
	def testAccept(self, i, o):
		_ = ParseRequestHeader('ACCEPT', i)
		for i, n in enumerate(_):
			ASSERT_IS_EQUAL(n.type, o[i]['type'])
			ASSERT_IS_EQUAL(n.mimetype, o[i]['mimetype'])
			ASSERT_IS_EQUAL(n.subtype, o[i]['subtype'])
			ASSERT_IS_EQUAL(n.q, o[i]['q'])
		return

	@Parameterized(
		{
			'i': 'deflate, gzip;q=1.0, *;q=0.5',
			'o': [
				{'compression': 'deflate', 'q': 1.0},
				{'compression': 'gzip', 'q': 1.0},
				{'compression': '*', 'q': 0.5},
			]
		},
	)
	@Order(102)
	def testAcceptEncoding(self, i, o):
		_ = ParseRequestHeader('ACCEPT_ENCODING', i)
		for i, n in enumerate(_):
			ASSERT_IS_EQUAL(n.compression, o[i]['compression'])
			ASSERT_IS_EQUAL(n.q, o[i]['q'])
		return

	@Parameterized(
		{
			'i': 'no-cache, no-store',
			'o': {
				'no-cache': True,
				'no-store': True,
				'max-age': None,
				'max-stable': None,
				'min-fresh': None,
				'no-transform': None,
				'only-if-cached': None,
			},
		},
		{
			'i': 'no-cache, max-age=31536000',
			'o': {
				'no-cache': True,
				'no-store': None,
				'max-age': 31536000,
				'max-stable': None,
				'min-fresh': None,
				'no-transform': None,
				'only-if-cached': None,
			}, 
		},
	)
	@Order(103)
	def testCacheControl(self, i, o):
		_ = ParseRequestHeader('CACHE_CONTROL', i)
		ASSERT_IS_EQUAL(_.noCache, o['no-cache'])
		ASSERT_IS_EQUAL(_.noStore, o['no-store'])
		ASSERT_IS_EQUAL(_.maxAge, o['max-age'])
		ASSERT_IS_EQUAL(_.maxStable, o['max-stable'])
		ASSERT_IS_EQUAL(_.minFresh, o['min-fresh'])
		ASSERT_IS_EQUAL(_.noTransform, o['no-transform'])
		ASSERT_IS_EQUAL(_.onlyIfCached, o['only-if-cached'])
		return

	@Parameterized(
		{'i': 'keep-alive', 'o': 'keep-alive'},
		{'i': 'close', 'o': 'close' },
	)
	@Order(104)
	def testConnection(self, i, o):
		_ = ParseRequestHeader('CONNECTION', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': 'Tue, 11 Feb 2025 18:00:40 GMT', 'o': 'Tue, 11 Feb 2025 18:00:40 GMT' },
	)
	@Order(105)
	def testDate(self, i, o):
		_ = ParseRequestHeader('DATE', i)
		ASSERT_IS_EQUAL(isinstance(_, datetime), True)
		return

	@Parameterized(
		{'i': 'timeout=5, max=200', 'o': {'timeout':'5','max':'200'} },
	)
	@Order(106)
	def testKeepAlive(self, i, o):
		_ = ParseRequestHeader('KEEP_ALIVE', i)
		ASSERT_IS_EQUAL(_.timeout, o['timeout'])
		ASSERT_IS_EQUAL(_.max, o['max'])
		return

	@Parameterized(
		{'i': 'https://bad.example; rel="preconnect"', 'o': [{'reference':'https://bad.example','parameters':{'rel':'preconnect'}}] },
		{
			'i': '<https://one.example.com>; rel="preconnect", <https://two.example.com>; rel="preconnect", <https://three.example.com>; rel="preconnect"',
			'o': [
				{'reference':'https://one.example.com','parameters':{'rel':'preconnect'}},
				{'reference':'https://two.example.com','parameters':{'rel':'preconnect'}},
				{'reference':'https://three.example.com','parameters':{'rel':'preconnect'}},
			]
		},
	)
	@Order(107)
	def testLink(self, i, o):
		_ = ParseRequestHeader('LINK', i)
		for i, n in enumerate(_):
			ASSERT_IS_EQUAL(n.url, o[i]['reference'])
			ASSERT_IS_EQUAL(n.rel, o[i]['parameters']['rel'])
			ASSERT_IS_EQUAL(n.parameters, o[i]['parameters'])
		return

	@Parameterized(
		{'i': 'no-cache', 'o': 'no-cache'},
	)
	@Order(108)
	def testPragma(self, i, o):
		_ = ParseRequestHeader('PRAGMA', i)
		ASSERT_IS_EQUAL(_, o)
		return
	
	@Parameterized(
		{'i': 'u=1', 'o': {'u': 1, 'i': None}},
		{'i': 'i', 'o': {'u': None, 'i': True}},
		{'i': 'u=1, i', 'o': {'u': 1, 'i': True}},
	)
	@Order(109)
	def testPriority(self, i, o):
		_ = ParseRequestHeader('PRIORITY', i)
		ASSERT_IS_EQUAL(_.urgency, o['u'])
		ASSERT_IS_EQUAL(_.incremental, o['i'])
		return

	@Parameterized(
		{'i': 'example/1, foo/2', 'o': [
			{'protocol':'example','version':'1'},
			{'protocol':'foo','version':'2'},
		]},
		{'i': 'protocol/version', 'o': [
			{'protocol':'protocol','version':'version'},
		]},
	)
	@Order(110)
	def testUpgrade(self, i, o):
		_ = ParseRequestHeader('UPGRADE', i)
		for i, n in enumerate(_):
			ASSERT_IS_EQUAL(n.protocol, o[i]['protocol'])
			ASSERT_IS_EQUAL(n.version, o[i]['version'])
		return
	
	@Parameterized(
		{'i': '1.1 vegur', 'o': [
			{'protocolVersion':'1.1','protocol':None,'version':'1.1','host':'vegur','port':None},
		]},
		{'i': 'HTTP/1.1 GWA', 'o': [
			{'protocolVersion':'1.1','protocol':'HTTP','version':'1.1','host':'GWA','port':None},
		]},
		{'i': '1.0 fred, 1.1 p.example.net', 'o': [
			{'protocolVersion':'1.0','protocol':None,'version':'1.0','host':'fred','port':None},
			{'protocolVersion':'1.1','protocol':None,'version':'1.1','host':'p.example.net','port':None},
		]},
	)
	@Order(111)
	def testVia(self, i, o):
		_ = ParseRequestHeader('VIA', i)
		for i, n in enumerate(_):
			ASSERT_IS_EQUAL(n.protocol, o[i]['protocol'])
			ASSERT_IS_EQUAL(n.version, o[i]['version'])
			ASSERT_IS_EQUAL(n.host, o[i]['host'])
			ASSERT_IS_EQUAL(n.port, o[i]['port'])
		return

	@Parameterized(
		{'i': '110 anderson/1.3.37 "Response is stale"', 'o': {'code': '110', 'agent': 'anderson/1.3.37','text':'Response is stale','date':None}},
	)
	@Order(112)
	def testWarning(self, i, o):
		_ = ParseRequestHeader('WARNING', i)
		ASSERT_IS_EQUAL(_.code, o['code'])
		ASSERT_IS_EQUAL(_.agent, o['agent'])
		ASSERT_IS_EQUAL(_.text, o['text'])
		return

	# Content Headers
	# - CONTENT_DIGEST: ParseParameters()
	# - CONTENT_DISPOSISION: ParseStringWithParameters()
	# - CONTENT_DPR: ParseInteger()
	# - CONTENT_ENCODING: ParseList()
	# - CONTENT_LANGUAGE: ParseList()
	# - CONTENT_LENGTH: ParseInteger()
	# - CONTENT_LOCATION: ParseString()
	# - CONTENT_RANGE: ParseContentRange()
	# - CONTENT_SECURITY_POLICY: ParseParameters(sep=';', paramsep=' ')
	# - CONTENT_SECURITY_POLICY_REPORT_ONLY: ParseParameters(sep=';', paramsep=' ')
	# - CONTENT_TYPE: ParseContentType()
	# - ETAG: ParseETag()
	# - LAST_MODIFIED: ParseDate()
	# - REPR_DIGEST: ParseParameters()
	# - TRAILER: ParseString()
	# - TRANSFER_ENCODING: ParseList()
	# - WANT_CONTENT_DIGEST: ParseParameters()
	# - WANT_REPR_DIGEST: ParseParameters()
	@Parameterized(
		{'i': 'sha-256=10, sha=3', 'o': {'sha-256': '10', 'sha': '3'}},
	)
	@Order(201)
	def testContentDigest(self, i, o):
		_ = ParseRequestHeader('Content-Digest', i)
		ASSERT_IS_EQUAL(_, o)
		return
	
	@Parameterized(
		{'i': 'inline', 'o': {'value': 'inline', 'params': {}}},
		{'i': 'attachment; filename="filename"', 'o': {'value': 'attachment', 'params': {'filename':'filename'}}},
		{'i': 'form-data; name="name"; filename="filename"', 'o': {'value': 'form-data', 'params': {'name':'name','filename':'filename'}}},
	)
	@Order(202)
	def testContentDisposition(self, i, o):
		v, params = ParseRequestHeader('Content-Disposition', i)
		ASSERT_IS_EQUAL(v, o['value'])
		ASSERT_IS_EQUAL(params, o['params'])
		return
	
	@Parameterized(
		{'i': '1', 'o': 1},
	)
	@Order(203)
	def testContentDPR(self, i, o):
		_ = ParseRequestHeader('Content-DPR', i)
		ASSERT_IS_EQUAL(_, o)
		return
	
	@Parameterized(
		{'i': 'deflate, gzip', 'o': ['deflate','gzip']},
	)
	@Order(204)
	def testContentEncoding(self, i, o):
		_ = ParseRequestHeader('Content-Encoding', i)
		ASSERT_IS_EQUAL(_, o)
		return
	
	@Parameterized(
		{'i': 'en, kr, ko-KR', 'o': ['en','kr','ko-KR']},
	)
	@Order(205)
	def testContentLanguage(self, i, o):
		_ = ParseRequestHeader('Content-Language', i)
		ASSERT_IS_EQUAL(_, o)
		return
	
	@Parameterized(
		{'i': '123232', 'o': 123232},
	)
	@Order(206)
	def testContentLength(self, i, o):
		_ = ParseRequestHeader('Content-Length', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': '/', 'o': '/'},
		{'i': 'https://www.example.com', 'o': 'https://www.example.com'},
		{'i': '"https://www.example.com"', 'o': 'https://www.example.com'},
	)
	@Order(207)
	def testContentLocation(self, i, o):
		_ = ParseRequestHeader('Content-Location', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': 'bytes 200-1000/67589', 'o': {'unit':'bytes','start':200,'end':1000,'size':67589}},
	)
	@Order(208)
	def testContentRange(self, i, o):
		_ = ParseRequestHeader('Content-Range', i)
		ASSERT_IS_EQUAL(_.unit, o['unit'])
		ASSERT_IS_EQUAL(_.start, o['start'])
		ASSERT_IS_EQUAL(_.end, o['end'])
		ASSERT_IS_EQUAL(_.size, o['size'])
		return

	@Parameterized(
		{'i': 'a; b; c', 'o': {'a':None,'b':None,'c':None}},
		{'i': 'eport-uri https://endpoint.example.com; report-to endpoint_name', 'o': {'eport-uri':'https://endpoint.example.com','report-to':'endpoint_name'}},
	)
	@Order(209)
	def testContentSecurityPolicy(self, i, o):
		_ = ParseRequestHeader('Content-Security-Policy', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': 'a; b; c', 'o': {'a':None,'b':None,'c':None}},
		{'i': 'default-src https:; report-uri /csp-report-url/; report-to csp-endpoint;', 'o': {'default-src':'https:','report-uri':'/csp-report-url/','report-to':'csp-endpoint'}},
	)
	@Order(210)
	def testContentSecurityPolicyReportOnly(self, i, o):
		_ = ParseRequestHeader('Content-Security-Policy-Report-Only', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': 'application/json; charset=utf-8', 'o': {'type':'application/json','charset':'utf-8','boundary':None}},
		{'i': 'multipart/form-data; boundary=BoundaryString', 'o': {'type':'multipart/form-data','charset':None,'boundary':'BoundaryString'}},
	)
	@Order(211)
	def testContentType(self, i, o):
		_ = ParseRequestHeader('Content-Type', i)
		ASSERT_IS_EQUAL(_.type, o['type'])
		ASSERT_IS_EQUAL(_.charset, o['charset'])
		ASSERT_IS_EQUAL(_.boundary, o['boundary'])
		return

	@Parameterized(
		{'i': 'W/"0815"', 'o': {'weak': True, 'etag': '0815'}},
		{'i': '"33a64df551425fcc55e4d42a148795d9f25f89d4"', 'o': {'weak':None,'etag':'33a64df551425fcc55e4d42a148795d9f25f89d4'}},
	)
	@Order(212)
	def testETag(self, i, o):
		_ = ParseRequestHeader('ETag', i)
		ASSERT_IS_EQUAL(_.weakvalidator, o['weak'])
		ASSERT_IS_EQUAL(_.etag, o['etag'])
		return

	@Parameterized(
		{'i': 'Tue, 11 Feb 2025 18:00:40 GMT', 'o': datetime.now() },
	)
	@Order(213)
	def testLastModified(self, i, o):
		_ = ParseRequestHeader('Last-Modified', i)
		ASSERT_IS_EQUAL(isinstance(_, datetime), True)
		return

	@Parameterized(
		{'i': 'sha-256=10, sha=3', 'o': {'sha-256': '10', 'sha': '3'}},
	)
	@Order(214)
	def testReprDigest(self, i, o):
		_ = ParseRequestHeader('Repr-Digest', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': 'X-Event', 'o': 'X-Event'},
	)
	@Order(215)
	def testTrailer(self, i, o):
		_ = ParseRequestHeader('Trailer', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': 'a, b, c', 'o': ['a','b','c']},
		{'i': 'gzip, chunked', 'o':['gzip', 'chunked']}
	)
	@Order(216)
	def testTransferEncoding(self, i, o):
		_ = ParseRequestHeader('Transfer-Encoding', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': 'sha-256=10, sha=3', 'o': {'sha-256': '10', 'sha': '3'}},
	)
	@Order(217)
	def testWantContentDigest(self, i, o):
		_ = ParseRequestHeader('Want-Content-Digest', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': 'sha-256=10, sha=3', 'o': {'sha-256': '10', 'sha': '3'}},
	)
	@Order(218)
	def testWantReprDigest(self, i, o):
		_ = ParseRequestHeader('Want-Repr-Digest', i)
		ASSERT_IS_EQUAL(_, o)
		return