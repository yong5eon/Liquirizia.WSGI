# -*- coding: utf-8 -*-

from Liquirizia.Test import *

from Liquirizia.WSGI.Header import *
from Liquirizia.WSGI.Headers import *

class TestHeader(Case):
	@Parameterized(
		{'i': 'application/json; charset=utf-8'},
	)
	@Order(0)
	def testHeader(self, i):
		_ = Header(i)
		ASSERT_IS_EQUAL(str(_), i)
		return

	@Parameterized(
		{'i': 'application/json; charset=utf-8', 'value': 'application/json', 'params': {'charset': 'utf-8'}},
	)
	@Order(1)
	def testHeaderWithParameters(self, i, value, params):
		_ = HeaderWithParameters(i)
		ASSERT_IS_EQUAL(str(_), i)
		ASSERT_IS_EQUAL(_.value, value)
		ASSERT_IS_EQUAL(_.parameters, params)
		return

	@Parameterized(
		{'i': 'a=1', 'o': {'key':'a','weight':'1'}},
		{'i': 'a', 'o': {'key':'a','weight': None}},
	)
	@Order(2)
	def testHeaderAsParameter(self, i, o):
		_ = HeaderAsParameter(i)
		ASSERT_IS_EQUAL(str(_), i)
		ASSERT_IS_EQUAL(_.key, o['key'])
		ASSERT_IS_EQUAL(_.weight, o['weight'])
		return

	@Parameterized(
		{'i': 'a=1,b=s,c=2.0', 'params': {'a':'1','b':'s','c':'2.0'}},
		{'i': 'a=1,b=s,c', 'params': {'a':'1','b':'s','c':None}},
	)
	@Order(3)
	def testHeaderAsParameters(self, i, params):
		_ = HeaderAsParameters(i)
		ASSERT_IS_EQUAL(str(_), i)
		ASSERT_IS_EQUAL(dict(_), params)
		return

	@Parameterized(
		{'i': 'a=1,b=s,c=2.0', 'o': ['a=1','b=s','c=2.0']},
	)
	@Order(4)
	def testHeaderAsList(self, i, o):
		_ = HeaderAsList(i)
		ASSERT_IS_EQUAL(str(_), i)
		ASSERT_IS_EQUAL([str(param) for param in _], o)
		return

	@Parameterized(
		{'i': 'a=1 b=s c=2.0,a=1 b=s c=2.0', 'o': [{'a':'1','b':'s','c':'2.0'},{'a':'1','b':'s','c':'2.0'}]},
	)
	@Order(5)
	def testHeaderAsParametersList(self, i, o):
		_ = HeaderAsList(i, format=HeaderAsParameters, options={'sep': ' '})
		ASSERT_IS_EQUAL(str(_), i)
		ASSERT_IS_EQUAL([dict(param) for param in _], o)
		return

	@Parameterized(
		{'i': 'application/json; charset=utf-8, text/plain; charset=utf-8', 'o': [
			{'value': 'application/json','params':{'charset':'utf-8'}},
			{'value': 'text/plain','params':{'charset':'utf-8'}},
		]},
	)
	@Order(6)
	def testHeaderAsWithParametersList(self, i, o):
		_ = HeaderAsList(i, format=HeaderWithParameters, options={'paramsep': ' '})
		ASSERT_IS_EQUAL(str(_), i)
		for i, n in enumerate(_):
			ASSERT_IS_EQUAL(n.value, o[i]['value'])
			ASSERT_IS_EQUAL(n.parameters, o[i]['params'])
		return
	
	@Parameterized(
		{
			'i': 'application/json, application/x-www-form-urlencoded; q=0.6, application/xml; q=0.7',
			'o': [
				{'value': 'application/json', 'q': 1.0, 'mimetype': 'application', 'subtype': 'json'},
				{'value': 'application/xml', 'q': 0.7, 'mimetype': 'application', 'subtype': 'xml'},
				{'value': 'application/x-www-form-urlencoded', 'q': 0.6, 'mimetype': 'application', 'subtype': 'x-www-form-urlencoded'},
			]
		},
	)
	@Order(7)
	def testAccept(self, i, o):
		_ = Accept(i)
		for i, n in enumerate(_):
			ASSERT_IS_EQUAL(n.value, o[i]['value'])
			ASSERT_IS_EQUAL(n.mimetype, o[i]['mimetype'])
			ASSERT_IS_EQUAL(n.subtype, o[i]['subtype'])
			ASSERT_IS_EQUAL(n.q, o[i]['q'])
		return

	@Parameterized(
		{
			'i': 'deflate, gzip;q=1.0, *;q=0.5',
			'o': [
				{'directive': 'deflate', 'q': 1.0},
				{'directive': 'gzip', 'q': 1.0},
				{'directive': '*', 'q': 0.5},
			]
		},
	)
	@Order(8)
	def testAcceptEncoding(self, i, o):
		_ = AcceptEncoding(i)
		for i, n in enumerate(_):
			ASSERT_IS_EQUAL(n.directive, o[i]['directive'])
			ASSERT_IS_EQUAL(n.q, o[i]['q'])
		return

	@Parameterized(
		{
			'i': 'no-cache, no-store, must-revalidate',
			'o': [
				{'directive': 'no-cache', 'seconds': None},
				{'directive': 'no-store', 'seconds': None},
				{'directive': 'must-revalidate', 'seconds': None},
			]
		},
		{
			'i': 'public, max-age=31536000',
			'o': [
				{'directive': 'public', 'seconds': None},
				{'directive': 'max-age', 'seconds': 31536000},
			]
		},

	)
	@Order(9)
	def testCacheControl(self, i, o):
		_ = CacheControl(i)
		for i, n in enumerate(_):
			ASSERT_IS_EQUAL(n.directive, o[i]['directive'])
			ASSERT_IS_EQUAL(n.seconds, o[i]['seconds'])
		return

	@Parameterized(
		{'i': 'keep-alive', 'o': 'keep-alive'},
		{'i': 'close', 'o': 'close' },
	)
	@Order(10)
	def testConnection(self, i, o):
		_ = Connection(i)
		ASSERT_IS_EQUAL(str(_), o)
		return

	@Parameterized(
		{'i': 'Tue, 11 Feb 2025 18:00:40 GMT', 'o': 'Tue, 11 Feb 2025 18:00:40 GMT' },
	)
	@Order(11)
	def testDate(self, i, o):
		_ = Date(i)
		ASSERT_IS_EQUAL(str(_), o)
		return

	@Parameterized(
		{'i': 'timeout=5, max=200', 'o': {'timeout':'5','max':'200'} },
	)
	@Order(12)
	def testKeepAlive(self, i, o):
		_ = KeepAlive(i)
		ASSERT_IS_EQUAL(dict(_), o)
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
	@Order(13)
	def testLink(self, i, o):
		_ = Link(i)
		for i, n in enumerate(_):
			ASSERT_IS_EQUAL(n.reference, o[i]['reference'])
			ASSERT_IS_EQUAL(n.parameters, o[i]['parameters'])
		return

	@Parameterized(
		{'i': 'no-cache', 'o': 'no-cache'},
	)
	@Order(14)
	def testPragma(self, i, o):
		_ = Pragma(i)
		ASSERT_IS_EQUAL(str(_), o)
		return

	@Parameterized(
		{'i': 'u=1', 'o': {'u': '1', 'i': False}},
		{'i': 'i', 'o': {'u': None, 'i': True}},
		{'i': 'u=1, i', 'o': {'u': '1', 'i': True}},
	)
	@Order(15)
	def testPriority(self, i, o):
		_ = Priority(i)
		ASSERT_IS_EQUAL(_.u, o['u'])
		ASSERT_IS_EQUAL(_.i, o['i'])
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
	@Order(16)
	def testUpgrade(self, i, o):
		_ = Upgrade(i)
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
	@Order(17)
	def testVia(self, i, o):
		_ = Via(i)
		for i, n in enumerate(_):
			ASSERT_IS_EQUAL(n.protocol, o[i]['protocol'])
			ASSERT_IS_EQUAL(n.version, o[i]['version'])
		return

	@Parameterized(
		{'i': '110 anderson/1.3.37 "Response is stale"', 'o': {'code': '110', 'agent': 'anderson/1.3.37','text':'"Response is stale"'}},
		# {'i': '112 - "cache down" "Wed, 21 Oct 2015 07:28:00 GMT"', 'o': {'code': '110', 'agent': 'anderson/1.3.37','text':'Response is stale'}},
	)
	@Order(18)
	def testWarning(self, i, o):
		_ = Warning(i)
		ASSERT_IS_EQUAL(str(_), i)
		return

	@Parameterized(
		{'i': 'sha-256=10, sha=3', 'o': {'sha-256': '10', 'sha': '3'}},
	)
	@Order(19)
	def testContentDigest(self, i, o):
		_ = ContentDigest(i)
		ASSERT_IS_EQUAL(dict(_), o)
		return

	@Parameterized(
		{'i': 'inline', 'o': {'value': 'inline', 'params': {}}},
		{'i': 'attachment; filename="filename"', 'o': {'value': 'attachment', 'params': {'filename':'filename'}}},
		{'i': 'form-data; name="name"; filename="filename"', 'o': {'value': 'form-data', 'params': {'name':'name','filename':'filename'}}},
	)
	@Order(20)
	def testContentDisposition(self, i, o):
		_ = ContentDisposition(i)
		ASSERT_IS_EQUAL(_.value, o['value'])
		ASSERT_IS_EQUAL(_.parameters, o['params'])
		return

	@Parameterized(
		{'i': '1', 'o': '1'},
	)
	@Order(21)
	def testContentDPR(self, i, o):
		_ = ContentDPR(i)
		ASSERT_IS_EQUAL(str(_), o)
		return

	@Parameterized(
		{'i': 'deflate, gzip', 'o': ['deflate','gzip']},
	)
	@Order(22)
	def testContentEncoding(self, i, o):
		_ = ContentEncoding(i)
		ASSERT_IS_EQUAL([str(h) for h in _], o)
		return

	@Parameterized(
		{'i': 'en, kr, ko-KR', 'o': ['en','kr','ko-KR']},
	)
	@Order(23)
	def testContentLanguage(self, i, o):
		_ = ContentLanguage(i)
		ASSERT_IS_EQUAL([str(h) for h in _], o)
		return


	@Parameterized(
		{'i': '123232', 'o': 123232},
	)
	@Order(24)
	def testContentLength(self, i, o):
		_ = ContentLength(i)
		ASSERT_IS_EQUAL(int(str(_)), o)
		return

	@Parameterized(
		{'i': '/', 'o': '/'},
	)
	@Order(25)
	def testContentLocation(self, i, o):
		_ = ContentLocation(i)
		ASSERT_IS_EQUAL(str(_), o)
		return


	@Parameterized(
		{'i': 'bytes 200-1000/67589', 'o': {'unit':'bytes','offset':200,'end':1000,'size':67589}},
	)
	@Order(26)
	def testContentRange(self, i, o):
		_ = ContentRange(i)
		ASSERT_IS_EQUAL(_.unit, o['unit'])
		ASSERT_IS_EQUAL(_.offset, o['offset'])
		ASSERT_IS_EQUAL(_.end, o['end'])
		ASSERT_IS_EQUAL(_.size, o['size'])
		return

	@Parameterized(
		{'i': 'a; b; c', 'o': ['a','b','c']},
	)
	@Order(27)
	def testContentSecurityPolicy(self, i, o):
		_ = ContentSecurityPolicy(i)
		ASSERT_IS_EQUAL([str(h) for h in _], o)
		return

	@Parameterized(
		{'i': 'a; b; c', 'o': ['a','b','c']},
	)
	@Order(28)
	def testContentSecurityPolicyReportOnly(self, i, o):
		_ = ContentSecurityPolicyReportOnly(i)
		ASSERT_IS_EQUAL([str(h) for h in _], o)
		return

	@Parameterized(
		{'i': 'application/json; charset=utf-8', 'o': {'value':'application/json','charset':'utf-8','boundary':None}},
		{'i': 'multipart/form-data; boundary=BoundaryString', 'o': {'value':'multipart/form-data','charset':None,'boundary':'BoundaryString'}},
	)
	@Order(29)
	def testContentType(self, i, o):
		_ = ContentType(i)
		ASSERT_IS_EQUAL(_.value, o['value'])
		ASSERT_IS_EQUAL(_.charset, o['charset'])
		ASSERT_IS_EQUAL(_.boundary, o['boundary'])
		return

	@Parameterized(
		{'i': 'W/"0815"', 'o': '0815'},
		{'i': '"33a64df551425fcc55e4d42a148795d9f25f89d4"', 'o': '33a64df551425fcc55e4d42a148795d9f25f89d4'},
	)
	@Order(30)
	def testETag(self, i, o):
		_ = ETag(i)
		ASSERT_IS_EQUAL(_.etag, o)
		return

	@Parameterized(
		{'i': 'Tue, 11 Feb 2025 18:00:40 GMT', 'o': 'Tue, 11 Feb 2025 18:00:40 GMT' },
	)
	@Order(31)
	def testLastModified(self, i, o):
		_ = LastModified(i)
		ASSERT_IS_EQUAL(str(_), o)
		return

	@Parameterized(
		{'i': 'sha-256=10, sha=3', 'o': {'sha-256': '10', 'sha': '3'}},
	)
	@Order(32)
	def testReprDigest(self, i, o):
		_ = ReprDigest(i)
		ASSERT_IS_EQUAL(dict(_), o)
		return

	@Parameterized(
		{'i': 'X-Event', 'o': 'X-Event'},
	)
	@Order(33)
	def testTrailer(self, i, o):
		_ = Trailer(i)
		ASSERT_IS_EQUAL(str(_), o)
		return

	@Parameterized(
		{'i': 'a, b, c', 'o': ['a','b','c']},
	)
	@Order(34)
	def testTransferEncoding(self, i, o):
		_ = TransferEncoding(i)
		ASSERT_IS_EQUAL([str(h) for h in _], o)
		return

	@Parameterized(
		{'i': 'sha-256=10, sha=3', 'o': {'sha-256': '10', 'sha': '3'}},
	)
	@Order(35)
	def testReprContentDigest(self, i, o):
		_ = WantContentDigest(i)
		ASSERT_IS_EQUAL(dict(_), o)
		return

	@Parameterized(
		{'i': 'sha-256=10, sha=3', 'o': {'sha-256': '10', 'sha': '3'}},
	)
	@Order(36)
	def testWantReprDigest(self, i, o):
		_ = WantReprDigest(i)
		ASSERT_IS_EQUAL(dict(_), o)
		return

