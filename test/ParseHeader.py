# -*- coding: utf-8 -*-

from Liquirizia.Test import *
from Liquirizia.WSGI.Utils import ParseHeader

from datetime import datetime


class TestParseHeader(Case):
	# Common Headers
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
		_ = ParseHeader('ACCEPT', i)
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
		_ = ParseHeader('ACCEPT_ENCODING', i)
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
		_ = ParseHeader('CACHE_CONTROL', i)
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
		_ = ParseHeader('CONNECTION', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': 'Tue, 11 Feb 2025 18:00:40 GMT', 'o': 'Tue, 11 Feb 2025 18:00:40 GMT' },
	)
	@Order(105)
	def testDate(self, i, o):
		_ = ParseHeader('DATE', i)
		ASSERT_IS_EQUAL(isinstance(_, datetime), True)
		return

	@Parameterized(
		{'i': 'timeout=5, max=200', 'o': {'timeout':'5','max':'200'} },
	)
	@Order(106)
	def testKeepAlive(self, i, o):
		_ = ParseHeader('KEEP_ALIVE', i)
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
		_ = ParseHeader('LINK', i)
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
		_ = ParseHeader('PRAGMA', i)
		ASSERT_IS_EQUAL(_, o)
		return
	
	@Parameterized(
		{'i': 'u=1', 'o': {'u': 1, 'i': None}},
		{'i': 'i', 'o': {'u': None, 'i': True}},
		{'i': 'u=1, i', 'o': {'u': 1, 'i': True}},
	)
	@Order(109)
	def testPriority(self, i, o):
		_ = ParseHeader('PRIORITY', i)
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
		_ = ParseHeader('UPGRADE', i)
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
		_ = ParseHeader('VIA', i)
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
		_ = ParseHeader('WARNING', i)
		ASSERT_IS_EQUAL(_.code, o['code'])
		ASSERT_IS_EQUAL(_.agent, o['agent'])
		ASSERT_IS_EQUAL(_.text, o['text'])
		return

	# Content Headers
	@Parameterized(
		{'i': 'sha-256=10, sha=3', 'o': {'sha-256': '10', 'sha': '3'}},
	)
	@Order(201)
	def testContentDigest(self, i, o):
		_ = ParseHeader('Content-Digest', i)
		ASSERT_IS_EQUAL(_, o)
		return
	
	@Parameterized(
		{'i': 'inline', 'o': {'value': 'inline', 'params': {}}},
		{'i': 'attachment; filename="filename"', 'o': {'value': 'attachment', 'params': {'filename':'filename'}}},
		{'i': 'form-data; name="name"; filename="filename"', 'o': {'value': 'form-data', 'params': {'name':'name','filename':'filename'}}},
	)
	@Order(202)
	def testContentDisposition(self, i, o):
		v, params = ParseHeader('Content-Disposition', i)
		ASSERT_IS_EQUAL(v, o['value'])
		ASSERT_IS_EQUAL(params, o['params'])
		return
	
	@Parameterized(
		{'i': '1', 'o': 1},
	)
	@Order(203)
	def testContentDPR(self, i, o):
		_ = ParseHeader('Content-DPR', i)
		ASSERT_IS_EQUAL(_, o)
		return
	
	@Parameterized(
		{'i': 'deflate, gzip', 'o': ['deflate','gzip']},
	)
	@Order(204)
	def testContentEncoding(self, i, o):
		_ = ParseHeader('Content-Encoding', i)
		ASSERT_IS_EQUAL(_, o)
		return
	
	@Parameterized(
		{'i': 'en, kr, ko-KR', 'o': ['en','kr','ko-KR']},
	)
	@Order(205)
	def testContentLanguage(self, i, o):
		_ = ParseHeader('Content-Language', i)
		ASSERT_IS_EQUAL(_, o)
		return
	
	@Parameterized(
		{'i': '123232', 'o': 123232},
	)
	@Order(206)
	def testContentLength(self, i, o):
		_ = ParseHeader('Content-Length', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': '/', 'o': '/'},
		{'i': 'https://www.example.com', 'o': 'https://www.example.com'},
		{'i': '"https://www.example.com"', 'o': 'https://www.example.com'},
	)
	@Order(207)
	def testContentLocation(self, i, o):
		_ = ParseHeader('Content-Location', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': 'bytes 200-1000/67589', 'o': {'unit':'bytes','start':200,'end':1000,'size':67589}},
	)
	@Order(208)
	def testContentRange(self, i, o):
		_ = ParseHeader('Content-Range', i)
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
		_ = ParseHeader('Content-Security-Policy', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': 'a; b; c', 'o': {'a':None,'b':None,'c':None}},
		{'i': 'default-src https:; report-uri /csp-report-url/; report-to csp-endpoint;', 'o': {'default-src':'https:','report-uri':'/csp-report-url/','report-to':'csp-endpoint'}},
	)
	@Order(210)
	def testContentSecurityPolicyReportOnly(self, i, o):
		_ = ParseHeader('Content-Security-Policy-Report-Only', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': 'application/json; charset=utf-8', 'o': {'type':'application/json','charset':'utf-8','boundary':None}},
		{'i': 'multipart/form-data; boundary=BoundaryString', 'o': {'type':'multipart/form-data','charset':None,'boundary':'BoundaryString'}},
	)
	@Order(211)
	def testContentType(self, i, o):
		_ = ParseHeader('Content-Type', i)
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
		_ = ParseHeader('ETag', i)
		ASSERT_IS_EQUAL(_.weakvalidator, o['weak'])
		ASSERT_IS_EQUAL(_.etag, o['etag'])
		return

	@Parameterized(
		{'i': 'Tue, 11 Feb 2025 18:00:40 GMT', 'o': datetime.now() },
	)
	@Order(213)
	def testLastModified(self, i, o):
		_ = ParseHeader('Last-Modified', i)
		ASSERT_IS_EQUAL(isinstance(_, datetime), True)
		return

	@Parameterized(
		{'i': 'sha-256=10, sha=3', 'o': {'sha-256': '10', 'sha': '3'}},
	)
	@Order(214)
	def testReprDigest(self, i, o):
		_ = ParseHeader('Repr-Digest', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': 'X-Event', 'o': 'X-Event'},
	)
	@Order(215)
	def testTrailer(self, i, o):
		_ = ParseHeader('Trailer', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': 'a, b, c', 'o': ['a','b','c']},
		{'i': 'gzip, chunked', 'o':['gzip', 'chunked']}
	)
	@Order(216)
	def testTransferEncoding(self, i, o):
		_ = ParseHeader('Transfer-Encoding', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': 'sha-256=10, sha=3', 'o': {'sha-256': '10', 'sha': '3'}},
	)
	@Order(217)
	def testWantContentDigest(self, i, o):
		_ = ParseHeader('Want-Content-Digest', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': 'sha-256=10, sha=3', 'o': {'sha-256': '10', 'sha': '3'}},
	)
	@Order(218)
	def testWantReprDigest(self, i, o):
		_ = ParseHeader('Want-Repr-Digest', i)
		ASSERT_IS_EQUAL(_, o)
		return

	# Request Headers	
	@Parameterized(
		{
			'i': 'ko, en;q=1.0, *;q=0.5',
			'o': [
				{'language': 'ko', 'q': 1.0},
				{'language': 'en', 'q': 1.0},
				{'language': '*', 'q': 0.5},
			]
		},
	)
	@Order(301)
	def testAcceptLanguage(self, i, o):
		_ = ParseHeader('Accept-Language', i)
		for i, n in enumerate(_):
			ASSERT_IS_EQUAL(n.language, o[i]['language'])
			ASSERT_IS_EQUAL(n.q, o[i]['q'])
		return

	@Parameterized(
		{'i': 'example.com', 'o': {'host': 'example.com', 'port': None}},
		{'i': 'example.com:3333', 'o': {'host': 'example.com', 'port': 3333}},
	)
	@Order(302)
	def testAltUsed(self, i, o):
		_ = ParseHeader('Alt-Used', i)
		ASSERT_IS_EQUAL(_.host, o['host'])
		ASSERT_IS_EQUAL(_.port, o['port'])
		return

	@Parameterized(
		{'i': 'Basic YWxhZGRpbjpvcGVuc2VzYW1l', 'o': {'scheme': 'Basic', 'credentials': 'YWxhZGRpbjpvcGVuc2VzYW1l', 'params': {}}},
		{'i': 'Digest username="abc", password="def"', 'o': {'scheme': 'Digest', 'credentials': None, 'params': {'username':'abc','password':'def'}}},
	)
	@Order(303)
	def testAuthorization(self, i, o):
		_ = ParseHeader('Authorization', i)
		ASSERT_IS_EQUAL(_.scheme, o['scheme'])
		ASSERT_IS_EQUAL(_.credentials, o['credentials'])
		ASSERT_IS_EQUAL(_.parameters, o['params'])
		return
	
	@Parameterized(
		{
			'i': 'PHPSESSID=298zf09hf012fh2; csrftoken=u32t4o3tb3gg43; _gat=1;', 
			'o': [
				{'name':'PHPSESSID','value':'298zf09hf012fh2'},
				{'name':'csrftoken','value':'u32t4o3tb3gg43'},
				{'name':'_gat','value':'1'},
			],
		},
	)
	@Order(304)
	def testCookie(self, i, o):
		_ = ParseHeader('Cookie', i)
		for i, n in enumerate(_):
			ASSERT_IS_EQUAL(n.name, o[i]['name'])
			ASSERT_IS_EQUAL(n.value, o[i]['value'])
		return
	
	@Parameterized(
		{'i': '128', 'o': 128},
	)
	@Order(305)
	def testDeviceMemory(self, i, o):
		_ = ParseHeader('Device-Memory', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': '0', 'o': 0},
		{'i': '1', 'o': 1},
	)
	@Order(306)
	def testDNT(self, i, o):
		_ = ParseHeader('DNT', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': '1.7', 'o': 1.7},
	)
	@Order(307)
	def testDownlink(self, i, o):
		_ = ParseHeader('Downlink', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': '2.0', 'o': 2.0},
	)
	@Order(308)
	def testDPR(self, i, o):
		_ = ParseHeader('DPR', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': '1', 'o': 1},
	)
	@Order(309)
	def testEarlyData(self, i, o):
		_ = ParseHeader('Early-Data', i)
		ASSERT_IS_EQUAL(_, o)
		return
	
	@Parameterized(
		{'i': '4g', 'o': '4g'},
	)
	@Order(310)
	def testECT(self, i, o):
		_ = ParseHeader('ECT', i)
		ASSERT_IS_EQUAL(_, o)
		return
	
	@Parameterized(
		{'i': '100-continue', 'o': '100-continue'},
	)
	@Order(311)
	def testExpect(self, i, o):
		_ = ParseHeader('Expect', i)
		ASSERT_IS_EQUAL(_, o)
		return
	
	@Parameterized(
		{'i': 'for=192.0.2.60;proto=http;by=203.0.113.43', 'o': [{'for':'192.0.2.60','proto':'http','by':'203.0.113.43'}]},
		{'i': 'for=192.0.2.43, for=198.51.100.17', 'o': [{'for':'192.0.2.43'},{'for':'198.51.100.17'}]},
	)
	@Order(312)
	def testForwarded(self, i, o):
		_ = ParseHeader('Forwarded', i)
		ASSERT_IS_EQUAL(_, o)
		return
	

	@Parameterized(
		{'i': 'webmaster@example.org', 'o': 'webmaster@example.org'},
	)
	@Order(313)
	def testFrom(self, i, o):
		_ = ParseHeader('From', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': 'developer.mozilla.org', 'o': 'developer.mozilla.org'},
	)
	@Order(314)
	def testHost(self, i, o):
		_ = ParseHeader('Host', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': '"bfc13a64729c4290ef5b2c2730249c88ca92d82d"', 'o': ['bfc13a64729c4290ef5b2c2730249c88ca92d82d']},
		{'i': '"67ab43", "54ed21", "7892dd"', 'o': ['67ab43','54ed21','7892dd']},
		{'i': '*', 'o': ['*']},
	)
	@Order(315)
	def testIfMatch(self, i, o):
		_ = ParseHeader('If-Match', i)
		ASSERT_IS_EQUAL(_, o)
		return
	
	@Parameterized(
		{'i': 'Tue, 11 Feb 2025 18:00:40 GMT', 'o': datetime.now() },
	)
	@Order(316)
	def testIfModeifiedSince(self, i, o):
		_ = ParseHeader('If-Modified-Since', i)
		ASSERT_IS_EQUAL(isinstance(_, datetime), True)
		return

	@Parameterized(
		{'i': '"bfc13a64729c4290ef5b2c2730249c88ca92d82d"', 'o': ['bfc13a64729c4290ef5b2c2730249c88ca92d82d']},
		{'i': '"67ab43", "54ed21", "7892dd"', 'o': ['67ab43','54ed21','7892dd']},
		{'i': '*', 'o': ['*']},
	)
	@Order(317)
	def testIfNoneMatch(self, i, o):
		_ = ParseHeader('If-None-Match', i)
		ASSERT_IS_EQUAL(_, o)
		return
	
	@Parameterized(
		{'i': 'Wed, 21 Oct 2015 07:28:00 GMT', 'o': datetime.now()},
		{'i': '"67ab43"', 'o': '67ab43'},
	)
	@Order(318)
	def testIfRange(self, i, o):
		_ = ParseHeader('If-Range', i)
		if isinstance(o, str): ASSERT_IS_EQUAL(_, o)
		else: ASSERT_IS_EQUAL(isinstance(_, datetime), True)
		return
	
	@Parameterized(
		{'i': 'Tue, 11 Feb 2025 18:00:40 GMT', 'o': datetime.now() },
	)
	@Order(319)
	def testIfUnmodeifiedSince(self, i, o):
		_ = ParseHeader('If-Unmodified-Since', i)
		ASSERT_IS_EQUAL(isinstance(_, datetime), True)
		return	
	
	@Parameterized(
		{'i': '4', 'o': 4},
	)
	@Order(320)
	def testMaxForwards(self, i, o):
		_ = ParseHeader('Max-Forwards', i)
		ASSERT_IS_EQUAL(_, o)
		return
	
	@Parameterized(
		{'i': 'https://developer.mozilla.org', 'o': 'https://developer.mozilla.org'},
		{'i': 'https://developer.mozilla.org:80', 'o': 'https://developer.mozilla.org:80'},
	)
	@Order(321)
	def testOrigin(self, i, o):
		_ = ParseHeader('Origin', i)
		ASSERT_IS_EQUAL(_, o)
		return
	
	@Parameterized(
		{'i': 'Basic YWxhZGRpbjpvcGVuc2VzYW1l', 'o': {'scheme': 'Basic', 'credentials': 'YWxhZGRpbjpvcGVuc2VzYW1l'}},
		{'i': 'Bearer kNTktNTA1My00YzLT1234', 'o': {'scheme': 'Bearer', 'credentials': 'kNTktNTA1My00YzLT1234'}},
	)
	@Order(322)
	def testProxyAuthorization(self, i, o):
		_ = ParseHeader('Proxy-Authorization', i)
		ASSERT_IS_EQUAL(_.scheme, o['scheme'])
		ASSERT_IS_EQUAL(_.credentials, o['credentials'])
		return

	@Parameterized(
		{'i': 'bytes=0-499', 'o': {'unit': 'bytes', 'ranges': [{'start':0, 'end':499, 'suffixLength':None}]}},
		{'i': 'bytes=900-', 'o': {'unit': 'bytes', 'ranges': [{'start':900, 'end':None, 'suffixLength':None}]}},
		{'i': 'bytes=-100', 'o': {'unit': 'bytes', 'ranges': [{'start':None, 'end':None, 'suffixLength':100}]}},
		{'i': 'bytes=200-999, 2000-2499, 9500-', 'o': {'unit': 'bytes', 'ranges':[{'start':200, 'end':999, 'suffixLength':None},{'start':2000, 'end':2499, 'suffixLength':None},{'start':9500, 'end':None, 'suffixLength':None}]}},
		{'i': 'bytes=0-499, -499', 'o': {'unit': 'bytes', 'ranges': [{'start':0, 'end':499, 'suffixLength':None},{'start':None, 'end':None, 'suffixLength':499}]}},
	)
	@Order(322)
	def testRange(self, i, o):
		unit, ranges = ParseHeader('Range', i)
		ASSERT_IS_EQUAL(unit, o['unit'])
		for i, range in enumerate(ranges):
			ASSERT_IS_EQUAL(range.start, o['ranges'][i]['start'])
			ASSERT_IS_EQUAL(range.end, o['ranges'][i]['end'])
			ASSERT_IS_EQUAL(range.suffixLength, o['ranges'][i]['suffixLength'])
		return
	
	@Parameterized(
		{'i': 'https://developer.mozilla.org/en-US/docs/Web/JavaScript', 'o': 'https://developer.mozilla.org/en-US/docs/Web/JavaScript'},
		{'i': 'https://example.com/page?q=123', 'o': 'https://example.com/page?q=123'},
	)
	@Order(323)
	def testReferer(self, i, o):
		_ = ParseHeader('Referer', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': '125', 'o': 125},
	)
	@Order(324)
	def testRTT(self, i, o):
		_ = ParseHeader('RTT', i)
		ASSERT_IS_EQUAL(_, o)
		return
	
	@Parameterized(
		{'i': 'on', 'o': 'on'},
	)
	@Order(325)
	def testSaveData(self, i, o):
		_ = ParseHeader('Save-Data', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': '[{configVersion: "chrome.1", modelVersion: "1", taxonomyVersion: "1", topic: 43, version: "chrome.1:1:1"}]', 'o': '[{configVersion: "chrome.1", modelVersion: "1", taxonomyVersion: "1", topic: 43, version: "chrome.1:1:1"}]'},
	)
	@Order(326)
	def testSecBrowsingTopics(self, i, o):
		_ = ParseHeader('Sec-Browsing-Topics', i)
		ASSERT_IS_EQUAL(_, o)
		return
	
	@Parameterized(
		{'i': '"dark"', 'o': 'dark'},
	)
	@Order(327)
	def testSecCHPrefersColorScheme(self, i, o):
		_ = ParseHeader('Sec-CH-Prefers-Color-Scheme', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': '"reduce"', 'o': 'reduce'},
	)
	@Order(328)
	def testSecCHPefersReducedMotion(self, i, o):
		_ = ParseHeader('Sec-CH-Prefers-Reduced-Motion', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': '"reduce"', 'o': 'reduce'},
	)
	@Order(329)
	def testSecCHPrefersReducedTransparency(self, i, o):
		_ = ParseHeader('Sec-CH-Prefers-Reduced-Transparency', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{
			'i': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
			'o': [
				{'brand':'Not A;Brand','significantVersion':'99'},
				{'brand':'Chromium','significantVersion':'98'},
				{'brand':'Google Chrome','significantVersion':'98'},
			]
		},
	)
	@Order(330)
	def testSecCHUA(self, i, o):
		_ = ParseHeader('Sec-CH-UA', i)
		for i, n in enumerate(_):
			ASSERT_IS_EQUAL(n.brand, o[i]['brand'])
			ASSERT_IS_EQUAL(n.significantVersion, o[i]['significantVersion'])
		return

	@Parameterized(
		{'i': '"x86"', 'o': 'x86'},
		{'i': '"Apple Silicon"', 'o': 'Apple Silicon'},
	)
	@Order(331)
	def testSecCHUAArch(self, i, o):
		_ = ParseHeader('Sec-CH-UA-Arch', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': '"64"', 'o': 64},
	)
	@Order(332)
	def testSecCHUABitness(self, i, o):
		_ = ParseHeader('Sec-CH-UA-Bitness', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': '"96.0.4664.110"', 'o': '96.0.4664.110'},
	)
	@Order(333)
	def testSecCHUAFullVersion(self, i, o):
		_ = ParseHeader('Sec-CH-UA-Full-Version', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{
			'i': ' " Not A;Brand";v="99.0.0.0", "Chromium";v="98.0.4750.0", "Google Chrome";v="98.0.4750.0"', 
			'o': [
				{'brand':'Not A;Brand','fullVersion':'99.0.0.0'},
				{'brand':'Chromium','fullVersion':'98.0.4750.0'},
				{'brand':'Google Chrome','fullVersion':'98.0.4750.0'},
			]
		},
	)
	@Order(334)
	def testSecCHUAFullVersionList(self, i, o):
		_ = ParseHeader('Sec-CH-UA-Full-Version-List', i)
		for i, n in enumerate(_):
			ASSERT_IS_EQUAL(n.brand, o[i]['brand'])
			ASSERT_IS_EQUAL(n.fullVersion, o[i]['fullVersion'])
		return

	@Parameterized(
		{'i': '?1', 'o': True},
		{'i': '?0', 'o': None},
		{'i': '?2', 'o': None},
	)
	@Order(335)
	def testSecCHUAMobile(self, i, o):
		_ = ParseHeader('Sec-CH-UA-Mobile', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': '"Pixel 3 XL"', 'o': 'Pixel 3 XL'},
	)
	@Order(336)
	def testSecCHUAModel(self, i, o):
		_ = ParseHeader('Sec-CH-UA-Model', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': '"Android"', 'o': 'Android'},
		{'i': '"Linux"', 'o': 'Linux'},
		{'i': '"iOS"', 'o': 'iOS'},
		{'i': '"Windows"', 'o': 'Windows'},
	)
	@Order(337)
	def testSecCHPlatform(self, i, o):
		_ = ParseHeader('Sec-CH-UA-Platform', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': '"10.0.0"', 'o': '10.0.0'},
	)
	@Order(338)
	def testSecCHUAPlatformVersion(self, i, o):
		_ = ParseHeader('Sec-CH-UA-Platform-Version', i)
		ASSERT_IS_EQUAL(_, o)
		return
	
	@Parameterized(
		{'i': 'audio', 'o': 'audio'},
	)
	@Order(340)
	def testSecFetchDest(self, i, o):
		_ = ParseHeader('Sec-Fetch-Dest', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': 'cors', 'o': 'cors'},
	)
	@Order(341)
	def testSecFetchMode(self, i, o):
		_ = ParseHeader('Sec-Fetch-Mode', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': 'cross-site', 'o': 'cross-site'},
	)
	@Order(342)
	def testSetFetchSite(self, i, o):
		_ = ParseHeader('Sec-Fetch-Site', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': '?1', 'o': True},
		{'i': '?0', 'o': None},
		{'i': '1', 'o': None},
	)
	@Order(343)
	def testSecFetchUser(self, i, o):
		_ = ParseHeader('Sec-Fetch-User', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': '1', 'o': True},
		{'i': '0', 'o': None},
	)
	@Order(344)
	def testSecGPC(self, i, o):
		_ = ParseHeader('Sec-GPC', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': 'prefetch', 'o': 'prefetch'},
	)
	@Order(345)
	def testSecPurpose(self, i, o):
		_ = ParseHeader('Sec-Purpose', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': 'script', 'o': 'script'},
	)
	@Order(346)
	def testServiceWorker(self, i, o):
		_ = ParseHeader('Service-Worker', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': 'true', 'o': 'true'},
		{'i': 'json_fragment1', 'o': 'json_fragment1'},
	)
	@Order(347)
	def testServiceWorkerNavigationPreload(self, i, o):
		_ = ParseHeader('Service-Worker-Navigation-Preload', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': 'compress', 'o': [{'transferCoding':'compress','q':1.0}]},
		{'i': 'deflate', 'o': [{'transferCoding':'deflate','q':1.0}]},
		{'i': 'gzip', 'o': [{'transferCoding':'gzip','q':1.0}]},
		{'i': 'trailers', 'o': [{'transferCoding':'trailers','q':1.0}]},
		{'i': 'trailers, deflate;q=0.5', 'o': [{'transferCoding':'trailers','q':1.0},{'transferCoding':'deflate','q':0.5}]},
	)
	@Order(348)
	def testTE(self, i, o):
		_ = ParseHeader('TE', i)
		for i, n in enumerate(_):
			ASSERT_IS_EQUAL(n.transferCoding, o[i]['transferCoding'])
			ASSERT_IS_EQUAL(n.q, o[i]['q'])
		return

	@Parameterized(
		{'i': '1', 'o': True},
		{'i': '0', 'o': None},
	)
	@Order(349)
	def testUpgradeInsecureRequests(self, i, o):
		_ = ParseHeader('Upgrade-InSecure-Requests', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{
			'i': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0', 
			'o': {
				'product': 'Mozilla',
				'version': '5.0',
				'comment': '(Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0',
				'system': 'Windows NT 6.1; Win64; x64; rv:47.0',
				'platform': 'Gecko/20100101',
				'platformDetails': None,
				'extensions': ['Firefox/47.0']
			}
		},
		{
			'i': 'Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0',
			'o': {
				'product': 'Mozilla',
				'version': '5.0',
				'comment': '(Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0',
				'system': 'Macintosh; Intel Mac OS X x.y; rv:42.0',
				'platform': 'Gecko/20100101',
				'platformDetails': None,
				'extensions': ['Firefox/42.0']
			}
		},
		{
			'i': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
			'o': {
				'product': 'Mozilla',
				'version': '5.0',
				'comment': '(X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
				'system': 'X11; Linux x86_64',
				'platform': 'AppleWebKit/537.36',
				'platformDetails': 'KHTML, like Gecko',
				'extensions': ['Chrome/51.0.2704.103','Safari/537.36']
			}
		},
		{
			'i': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41',
			'o': {
				'product': 'Mozilla',
				'version': '5.0',
				'comment': '(X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41',
				'system': 'X11; Linux x86_64',
				'platform': 'AppleWebKit/537.36',
				'platformDetails': 'KHTML, like Gecko',
				'extensions': ['Chrome/51.0.2704.106','Safari/537.36','OPR/38.0.2220.41']
			}
		},
		{
			'i': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59',
			'o': {
				'product': 'Mozilla',
				'version': '5.0',
				'comment': '(Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59',
				'system': 'Windows NT 10.0; Win64; x64',
				'platform': 'AppleWebKit/537.36',
				'platformDetails': 'KHTML, like Gecko',
				'extensions': ['Chrome/91.0.4472.124','Safari/537.36','Edg/91.0.864.59']
			}
		},
		{
			'i': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Mobile/15E148 Safari/604.1',
			'o': {
				'product': 'Mozilla',
				'version': '5.0',
				'comment': '(iPhone; CPU iPhone OS 13_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Mobile/15E148 Safari/604.1',
				'system': 'iPhone; CPU iPhone OS 13_5_1 like Mac OS X',
				'platform': 'AppleWebKit/605.1.15',
				'platformDetails': 'KHTML, like Gecko',
				'extensions': ['Version/13.1.1','Mobile/15E148','Safari/604.1']
			}
		},
		{
			'i': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
			'o': {
				'product': 'Mozilla',
				'version': '5.0',
				'comment': '(compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
				'system': None,
				'platform': None,
				'platformDetails': None,
				'extensions': None
			}
		},
	)
	@Order(350)
	def testUserAgent(self, i, o):
		_ = ParseHeader('User-Agent', i)
		ASSERT_IS_EQUAL(_.product, o['product'])
		ASSERT_IS_EQUAL(_.version, o['version'])
		ASSERT_IS_EQUAL(_.comment, o['comment'])
		ASSERT_IS_EQUAL(_.system, o['system'])
		ASSERT_IS_EQUAL(_.platform, o['platform'])
		ASSERT_IS_EQUAL(_.platformDetails, o['platformDetails'])
		ASSERT_IS_EQUAL(_.extensions, o['extensions'])
		return

	@Parameterized(
		{'i': '343', 'o': 343},
	)
	@Order(338)
	def testViewportWidth(self, i, o):
		_ = ParseHeader('Viewport-Width', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': '1024', 'o': 1024},
	)
	@Order(351)
	def testWidth(self, i, o):
		_ = ParseHeader('Width', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': '203.0.113.195, 2001:db8:85a3:8d3:1319:8a2e:370:7348', 'o': ['203.0.113.195', '2001:db8:85a3:8d3:1319:8a2e:370:7348']},
		{'i': '203.0.113.195', 'o': ['203.0.113.195']},
	)
	@Order(352)
	def testXForwardedFor(self, i, o):
		_ = ParseHeader('X-Forwarded-For', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': 'id42.example-cdn.com', 'o': 'id42.example-cdn.com'},
	)
	@Order(353)
	def testXForwardedHost(self, i, o):
		_ = ParseHeader('X-Forwarded-Host', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': 'http', 'o': 'http'},
		{'i': 'https', 'o': 'https'},
	)
	@Order(354)
	def testXForwardedProto(self, i, o):
		_ = ParseHeader('X-Forwarded-Proto', i)
		ASSERT_IS_EQUAL(_, o)
		return

	# Response Headers
	@Parameterized(
		{'i': 'Viewport-Width, Width', 'o': ['Viewport-Width', 'Width']},
	)
	@Order(401)
	def testAcceptCH(self, i, o):
		_ = ParseHeader('Accept-CH', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': 'application/json', 'o': [('application/json',{})]},
		{'i': 'application/json, text/plain', 'o': [('application/json',{}),('text/plain',{})]},
		{'i': 'text/plain;charset=utf-8', 'o': [('text/plain',{'charset':'utf-8'})]},
	)
	@Order(402)
	def testAcceptPatch(self, i, o):
		_ = ParseHeader('Accept-Patch', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': 'application/json, text/plain', 'o': ['application/json','text/plain']},
		{'i': 'image/webp', 'o': ['image/webp']},
		{'i': '*/*', 'o': ['*/*']},
	)
	@Order(403)
	def testAcceptPost(self, i, o):
		_ = ParseHeader('Accept-Post', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': 'bytes', 'o': 'bytes'},
		{'i': 'none', 'o': 'none'},
	)
	@Order(404)
	def testAcceptRanges(self, i, o):
		_ = ParseHeader('Accept-Ranges', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': '24', 'o': 24},
	)
	@Order(405)
	def testAge(self, i, o):
		_ = ParseHeader('Age', i)
		ASSERT_IS_EQUAL(_, o)
		return
	
	@Parameterized(
		{'i': 'GET, POST, HEAD', 'o': ['GET', 'POST', 'HEAD']},
	)
	@Order(406)
	def testAllow(self, i, o):
		_ = ParseHeader('Allow', i)
		ASSERT_IS_EQUAL(_, o)
		return
	
	@Parameterized(
		{'i': 'h2=":443"; ma=2592000;', 'o': {'h2':':443','ma':'2592000'}},
		{'i': 'h2=":443"; ma=2592000; persist=1', 'o': {'h2':':443','ma':'2592000','persist':'1'}},
		{'i': 'h2="alt.example.com:443"; h3=":443"', 'o': {'h2':'alt.example.com:443','h3':':443'}},
		{'i': 'h3-25=":443"; ma=3600; h2=":443"; ma=3600', 'o': {'h3-25':':443','h2':':443','ma':'3600'}},
	)
	@Order(407)
	def testAltSvc(self, i, o):
		_ = ParseHeader('Alt-Svc', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': '"cache"', 'o': ['cache']},
		{'i': '"cache", "cookies"', 'o': ['cache','cookies']},
		{'i': '"*"', 'o': ['*']},
	)
	@Order(408)
	def testClearSiteData(self, i, o):
		_ = ParseHeader('Clear-Site-Data', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': 'Sec-CH-Prefers-Reduced-Motion', 'o': ['Sec-CH-Prefers-Reduced-Motion']},
	)
	@Order(409)
	def testCiriticalCH(self, i, o):
		_ = ParseHeader('Critical-CH', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': 'unsafe-none', 'o': 'unsafe-none'},
		{'i': 'require-corp', 'o': 'require-corp'},
		{'i': 'credentialless', 'o': 'credentialless'},
	)
	@Order(410)
	def testCrossOriginEmbedderPolicy(self, i, o):
		_ = ParseHeader('Cross-Origin-Embedder-Policy', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': 'unsafe-none', 'o': 'unsafe-none'},
		{'i': 'require-corp', 'o': 'require-corp'},
		{'i': 'credentialless', 'o': 'credentialless'},
	)
	@Order(411)
	def testCrossOriginOpenerPolicy(self, i, o):
		_ = ParseHeader('Cross-Origin-Opener-Policy', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': 'unsafe-none', 'o': 'unsafe-none'},
		{'i': 'require-corp', 'o': 'require-corp'},
		{'i': 'credentialless', 'o': 'credentialless'},
	)
	@Order(412)
	def testCrossOriginResourcePolicy(self, i, o):
		_ = ParseHeader('Cross-Origin-Resource-Policy', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': 'max-age=86400, enforce, report-uri="https://foo.example.com/report"', 'o': {
			'maxAge': 86400,
			'enforce': True,
			'reportUri': 'https://foo.example.com/report',
		}},
	)
	@Order(413)
	def testExpectCT(self, i, o):
		_ = ParseHeader('Expect-CT', i)
		ASSERT_IS_EQUAL(_.maxAge, o['maxAge'])
		ASSERT_IS_EQUAL(_.enforce, o['enforce'])
		ASSERT_IS_EQUAL(_.reportUri, o['reportUri'])
		return

	@Parameterized(
		{'i': 'Wed, 21 Oct 2015 07:28:00 GMT', 'o': datetime.now()},
	)
	@Order(414)
	def testExpires(self, i, o):
		_ = ParseHeader('Expires', i)
		ASSERT_IS_EQUAL(isinstance(_, datetime), True)
		return
	
	@Parameterized(
		{'i': '/index.html', 'o': '/index.html'},
	)
	@Order(415)
	def testLocation(self, i, o):
		_ = ParseHeader('Expires', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{
			'i': '{ "report_to": "name_of_reporting_group", "max_age": 12345, "include_subdomains": false, "success_fraction": 0.0, "failure_fraction": 1.0 }',
			'o': {
				'report_to': 'name_of_reporting_group',
				'max_age': 12345,
				'include_subdomains': False,
				'success_fraction': 0.0,
				'failure_fraction': 1.0,
			}
		},
	)
	@Order(416)
	def testNEL(self, i, o):
		_ = ParseHeader('NEL', i)
		ASSERT_IS_EQUAL(_, o)
		return
	
	@Parameterized(
		{
			'i': 'key-order',
			'o': {
				'keyOrder': True,
				'params': None,
				'excepts': None,
			}
		},
		{
			'i': 'params=("id")',
			'o': {
				'keyOrder': None,
				'params': ['id'],
				'excepts': None,
			}
		},
		{
			'i': 'params=("id" "order" "lang")',
			'o': {
				'keyOrder': None,
				'params': ['id','order','lang'],
				'excepts': None,
			}
		},
		{
			'i': 'params',
			'o': {
				'keyOrder': None,
				'params': True,
				'excepts': None,
			}
		},
		{
			'i': 'params, except=("id")',
			'o': {
				'keyOrder': None,
				'params': True,
				'excepts': ['id'],
			}
		},
	)
	@Order(417)
	def testNoVarySearch(self, i, o):
		_ = ParseHeader('No-Vary-Search', i)
		ASSERT_IS_EQUAL(_.keyOrder, o['keyOrder'])
		ASSERT_IS_EQUAL(_.params, o['params'])
		ASSERT_IS_EQUAL(_.excepts, o['excepts'])
		return
	
	@Parameterized(
		{'i': '?1', 'o': True},
		{'i': '?0', 'o': None},
		{'i': '1', 'o': None},
		{'i': '0', 'o': None},
	)
	@Order(418)
	def testObserveBrowsingTopics(self, i, o):
		_ = ParseHeader('Observe-Browsing-Topics', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': '?1', 'o': True},
		{'i': '?0', 'o': None},
		{'i': '1', 'o': None},
		{'i': '0', 'o': None},
	)
	@Order(419)
	def testOriginAgentCluster(self, i, o):
		_ = ParseHeader('Origin-Agent-Cluster', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{
			'i': 'picture-in-picture=(), geolocation=(self https://example.com/), camera=*',
			'o': [
				{'policy': 'picture-in-picture', 'args':[]},
				{'policy': 'geolocation', 'args':['self','https://example.com/']},
				{'policy': 'camera', 'args':['*']},
			],
		},
		{
			'i': 'picture-in-picture=()',
			'o': [
				{'policy': 'picture-in-picture', 'args':[]},
			],
		},
		{
			'i': 'geolocation=(self https://example.com/)',
			'o': [
				{'policy': 'geolocation', 'args':['self','https://example.com/']},
			], 
		},
		{
			'i': 'camera=*',
			'o': [
				{'policy': 'camera', 'args':['*']},
			],
		},
	)
	@Order(420)
	def testPermissionsPolicy(self, i, o):
		_ = ParseHeader('Permissions-Policy', i)
		for i, n in enumerate(_):
			ASSERT_IS_EQUAL(n.policy, o[i]['policy'])
			ASSERT_IS_EQUAL(n.args, o[i]['args'])
		return
	
	@Parameterized(
		{
			'i': 'Basic realm="Dev", charset="UTF-8"',
			'o': {
				'scheme': 'Basic',
				'token68': None,
				'parameters': {
					'realm': 'Dev',
					'charset': 'UTF-8'
				}
			},
		},
		{
			'i': 'Simple token68',
			'o': {
				'scheme': 'Simple',
				'token68': 'token68',
				'parameters': None, 
			},
		},

	)
	@Order(421)
	def testProxyAuthenticate(self, i, o):
		_ = ParseHeader('Proxy-Authenticate', i)
		ASSERT_IS_EQUAL(_.scheme, o['scheme'])
		ASSERT_IS_EQUAL(_.token68, o['token68'])
		ASSERT_IS_EQUAL(_.parameters, o['parameters'])
		return

	@Parameterized(
		{'i': 'strict-origin-when-cross-origin', 'o':['strict-origin-when-cross-origin']},
		{'i': 'strict-origin-when-cross-origin, origin-when-cross-origin', 'o':['strict-origin-when-cross-origin','origin-when-cross-origin']},
	)
	@Order(422)
	def testReferrerPolicy(self, i, o):
		_ = ParseHeader('Referrer-Policy', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': '5', 'o':{'time': 5,'url': None}},
		{'i': '5; url=https://example.com/', 'o':{'time': 5,'url': 'https://example.com/'}},
	)
	@Order(423)
	def testRefresh(self, i, o):
		_ = ParseHeader('Refresh', i)
		ASSERT_IS_EQUAL(_.time, o['time'])
		ASSERT_IS_EQUAL(_.url, o['url'])
		return

	# TODO: REPORT_TO: ParseJSON()
	@Parameterized(
		{
			'i': '{"group": "csp-endpoints", "max_age": 10886400, "endpoints": [{"url": "https://example.com/reports" },{ "url": "https://backup.com/reports"}]}', 
			'o': '{"group": "csp-endpoints", "max_age": 10886400, "endpoints": [{"url": "https://example.com/reports" },{ "url": "https://backup.com/reports"}]}'
		},
		{
			'i': '{"group": "csp-endpoints", "max_age": 10886400, "endpoints": [ { "url": "https://example.com/reports" }, { "url": "https://backup.com/reports" }]},{"a":"b"}', 
			'o': '{"group": "csp-endpoints", "max_age": 10886400, "endpoints": [ { "url": "https://example.com/reports" }, { "url": "https://backup.com/reports" }]},{"a":"b"}', 
		},
	)
	@Order(424)
	def testReportTo(self, i, o):
		_ = ParseHeader('Report-To', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{
			'i': 'csp-endpoint="https://example.com/csp-reports"', 
			'o': {
				'csp-endpoint': 'https://example.com/csp-reports'
			},
		},
		{
			'i': 'csp-endpoint="https://example.com/csp-reports", permissions-endpoint="https://example.com/permissions-policy-reports"', 
			'o': {
				'csp-endpoint': 'https://example.com/csp-reports',
				'permissions-endpoint': 'https://example.com/permissions-policy-reports',
			},
		},
	)
	@Order(425)
	def testReportingEndpoints(self, i, o):
		_ = ParseHeader('Reporting-Endpoints', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{
			'i': 'Wed, 21 Oct 2015 07:28:00 GMT', 
			'o': datetime.now(),
		},
		{
			'i': '120', 
			'o': 120,
		},
	)
	@Order(426)
	def testRetryAfter(self, i, o):
		_ = ParseHeader('Retry-After', i)
		if isinstance(o, int):
			ASSERT_IS_EQUAL(_, o)
		else:
			ASSERT_IS_EQUAL(isinstance(_, datetime), True)
		return
	
	@Parameterized(
		{
			'i': 'Apache/2.4.1 (Unix)', 
			'o': 'Apache/2.4.1 (Unix)'
		},
	)
	@Order(427)
	def testServer(self, i, o):
		_ = ParseHeader('Server', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{
			'i': 'missedCache', 
			'o': [{
				'name': 'missedCache',
				'duration': None,
				'description': None,
			}],
		},
		{
			'i': 'cpu;dur=2.4', 
			'o': [{
				'name': 'cpu',
				'duration': 2.4,
				'description': None,
			}],
		},
		{
			'i': 'cache;desc="Cache Read";dur=23.2', 
			'o': [{
				'name': 'cache',
				'duration': 23.2,
				'description': 'Cache Read',
			}],
		},
		{
			'i': 'db;dur=53, app;dur=47.2', 
			'o': [
				{
					'name': 'db',
					'duration': 53,
					'description': None,
				},
				{
					'name': 'app',
					'duration': 47.2,
					'description': None,
				},
			],
		},
	)
	@Order(428)
	def testServerTiming(self, i, o):
		_ = ParseHeader('Server-Timing', i)
		for i, st in enumerate(_):
			ASSERT_IS_EQUAL(st.name, o[i]['name'])
			ASSERT_IS_EQUAL(st.duration, o[i]['duration'])
			ASSERT_IS_EQUAL(st.description, o[i]['description'])
		return
	
	@Parameterized(
		{
			'i': 'a', 
			'o': 'a'
		},
	)
	@Order(429)
	def testServiceWorkerAllowed(self, i, o):
		_ = ParseHeader('Service-Worker-Allowed', i)
		ASSERT_IS_EQUAL(_, o)
		return
	
	# - SET_COOKIE: # TODO,
	@Parameterized(
		{
			'i': 'a', 
			'o': 'a'
		},
	)
	@Order(430)
	def testSetCookie(self, i, o):
		_ = ParseHeader('Set-Cookie', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{
			'i': 'logged-in', 
			'o': 'logged-in'
		},
	)
	@Order(431)
	def testSetLogin(self, i, o):
		_ = ParseHeader('Set-Login', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{
			'i': '/path/to/file.js.map', 
			'o': '/path/to/file.js.map'
		},
	)
	@Order(432)
	def testSourceMap(self, i, o):
		_ = ParseHeader('SourceMap', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{
			'i': '"/rules/prefetch.json"', 
			'o': ['/rules/prefetch.json']
		},
		{
			'i': '"/rules/prefetch.json","/rules/prerender.json"', 
			'o': ['/rules/prefetch.json','/rules/prerender.json']
		},
	)
	@Order(433)
	def testSpeculationRules(self, i, o):
		_ = ParseHeader('Speculation-Rules', i)
		ASSERT_IS_EQUAL(_, o)
		return
	
	@Parameterized(
		{
			'i': 'max-age=31536000; includeSubDomains', 
			'o': {
				'maxAge': 31536000,
				'includeSubDomains': True,
				'preload': None
			}
		},
		{
			'i': 'max-age=63072000; includeSubDomains; preload', 
			'o': {
				'maxAge': 63072000,
				'includeSubDomains': True,
				'preload': True
			}
		},
	)
	@Order(434)
	def testStrictTransportSecurity(self, i, o):
		_ = ParseHeader('Strict-Transport-Security', i)
		ASSERT_IS_EQUAL(_.maxAge, o['maxAge'])
		ASSERT_IS_EQUAL(_.includeSubDomains, o['includeSubDomains'])
		ASSERT_IS_EQUAL(_.preload, o['preload'])
		return
	
	@Parameterized(
		{
			'i': 'fenced-frame', 
			'o': 'fenced-frame'
		},
	)
	@Order(435)
	def testSupportsLoadingMode(self, i, o):
		_ = ParseHeader('Supports-Loading-Mode', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{
			'i': '*', 
			'o': ['*']
		},
		{
			'i': 'https://developer.mozilla.org', 
			'o': ['https://developer.mozilla.org']
		},
		{
			'i': '*, https://developer.mozilla.org', 
			'o': ['*', 'https://developer.mozilla.org']
		},
	)
	@Order(436)
	def testTimingAllowOrigin(self, i, o):
		_ = ParseHeader('Timing-Allow-Origin', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': '!', 'o': '!'},
		{'i': '?', 'o': '?'},
		{'i': 'G', 'o': 'G'},
		{'i': 'N', 'o': 'N'},
		{'i': 'T', 'o': 'T'},
		{'i': 'C', 'o': 'C'},
		{'i': 'P', 'o': 'P'},
		{'i': 'D', 'o': 'D'},
		{'i': 'U', 'o': 'U'},
	)
	@Order(437)
	def testTk(self, i, o):
		_ = ParseHeader('Tk', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{
			'i': '*', 
			'o': ['*']
		},
		{
			'i': 'Accept', 
			'o': ['Accept']
		},
		{
			'i': '*, Accept', 
			'o': ['*', 'Accept']
		},
	)
	@Order(438)
	def testVary(self, i, o):
		_ = ParseHeader('Vary', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{
			'i': 'Basic realm="Dev", charset="UTF-8"',
			'o': {
				'scheme': 'Basic',
				'token68': None,
				'parameters': {
					'realm': 'Dev',
					'charset': 'UTF-8'
				}
			},
		},
		{
			'i': 'Basic YWxhZGRpbjpvcGVuc2VzYW1l',
			'o': {
				'scheme': 'Basic',
				'token68': 'YWxhZGRpbjpvcGVuc2VzYW1l',
				'parameters': None, 
			},
		},

	)
	@Order(439)
	def testWWWAuthenticate(self, i, o):
		_ = ParseHeader('WWW-Authenticate', i)
		ASSERT_IS_EQUAL(_.scheme, o['scheme'])
		ASSERT_IS_EQUAL(_.token68, o['token68'])
		ASSERT_IS_EQUAL(_.parameters, o['parameters'])
		return

	@Parameterized(
		{'i': 'nosniff', 'o': 'nosniff'},
	)
	@Order(440)
	def testXContentTypeOptions(self, i, o):
		_ = ParseHeader('X-Content-Type-Options', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': 'on', 'o': True},
		{'i': 'off', 'o': False},
		{'i': '1', 'o': None},
		{'i': '0', 'o': None},
	)
	@Order(441)
	def testXDNSPrefetchControl(self, i, o):
		_ = ParseHeader('X-DNS-Prefetch-Control', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': 'DENY', 'o': 'DENY'},
		{'i': 'SAMEORIGIN', 'o': 'SAMEORIGIN'},
		{'i': 'ALLOW-FROM https://example.com', 'o': 'ALLOW-FROM https://example.com'},
	)
	@Order(442)
	def testXFrameOptions(self, i, o):
		_ = ParseHeader('X-Frame-Options', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': 'none', 'o': 'none'},
	)
	@Order(443)
	def testXPermittedCrossDomainPolicies(self, i, o):
		_ = ParseHeader('X-Permitted-Cross-Domain-Policies', i)
		ASSERT_IS_EQUAL(_, o)
		return
	
	@Parameterized(
		{'i': 'Liquirizia.WSGI', 'o': 'Liquirizia.WSGI'},
	)
	@Order(444)
	def testXPermittedCrossDomainPolicies(self, i, o):
		_ = ParseHeader('X-Powered-By', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{
			'i': 'BadBot: noindex, nofollow',
			'o': {
					'rules': ['noindex','nofollow'],
					'bot': 'BadBot',
			}
		},
		{
			'i': 'noindex, nofollow',
			'o': {
					'rules': ['noindex','nofollow'],
					'bot': None,
			}
		},
	)
	@Order(445)
	def testXRobotsTag(self, i, o):
		_ = ParseHeader('X-Robots-Tag', i)
		ASSERT_IS_EQUAL(_.rules, o['rules'])
		ASSERT_IS_EQUAL(_.bot, o['bot'])
		return

	# - X_XSS_PROTECTION: ParseXXSSProtection(), 
	@Parameterized(
		{
			'i': '0',
			'o': {
				'filtering': False,
				'parameters': None,
			}
		},
		{
			'i': '1',
			'o': {
				'filtering': True,
				'parameters': None,
			}
		},
		{
			'i': '1; mode=block',
			'o': {
				'filtering': True,
				'parameters': {
					'mode': 'block'
				},
			}
		},
		{
			'i': '1; report=https://example.com/report/to',
			'o': {
				'filtering': True,
				'parameters': {
					'report': 'https://example.com/report/to'
				},
			}
		},
	)
	@Order(446)
	def testXXSSProtection(self, i, o):
		_ = ParseHeader('X-XSS-Protection', i)
		ASSERT_IS_EQUAL(_.filtering, o['filtering'])
		ASSERT_IS_EQUAL(_.parameters, o['parameters'])
		return

	# CORS Headers
	@Parameterized(
		{'i': 'true', 'o': True},
		{'i': 'false', 'o': None},
	)
	@Order(501)
	def testAccessControlAllowCredentials(self, i, o):
		_ = ParseHeader('Access-Control-Allow-Credentials', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': 'X-Custom-Header, Upgrade-Insecure-Requests', 'o': ['X-Custom-Header', 'Upgrade-Insecure-Requests']},
		{'i': 'Accept', 'o': ['Accept']},
	)
	@Order(502)
	def testAccessControlAllowHeaders(self, i, o):
		_ = ParseHeader('Access-Control-Allow-Headers', i)
		ASSERT_IS_EQUAL(_, o)
		return
	
	@Parameterized(
		{'i': 'GET', 'o': ['GET']},
		{'i': 'GET, POST, PUT, DELETE', 'o': ['GET','POST','PUT','DELETE']},
	)
	@Order(503)
	def testAccessControlAllowMethods(self, i, o):
		_ = ParseHeader('Access-Control-Allow-Methods', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': '*', 'o': '*'},
		{'i': 'https://developer.mozilla.org', 'o': 'https://developer.mozilla.org'},
	)
	@Order(504)
	def testAccessControlAllowOrigin(self, i, o):
		_ = ParseHeader('Access-Control-Allow-Origin', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': 'Content-Encoding, Kuma-Revision', 'o': ['Content-Encoding','Kuma-Revision']},
		{'i': 'Content-Encoding', 'o': ['Content-Encoding']},
		{'i': '*', 'o': ['*']},
	)
	@Order(505)
	def testAccessControlExposeHeaders(self, i, o):
		_ = ParseHeader('Access-Control-Expose-Headers', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': '600', 'o': 600},
	)
	@Order(506)
	def testAccessControlMaxAge(self, i, o):
		_ = ParseHeader('Access-Control-Max-Age', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': 'Content-Type, Content-Encoding', 'o': ['Content-Type', 'Content-Encoding']},
		{'i': 'Content-Type', 'o': ['Content-Type']},
	)
	@Order(507)
	def testAccessControlRequestHeaders(self, i, o):
		_ = ParseHeader('Access-Control-Request-Headers', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': 'GET', 'o': 'GET'},
		{'i': 'POST', 'o': 'POST'},
		{'i': 'PUT', 'o': 'PUT'},
		{'i': 'DELETE', 'o': 'DELETE'},
	)
	@Order(508)
	def testAccessControlRequestMethod(self, i, o):
		_ = ParseHeader('Access-Control-Request-Method', i)
		ASSERT_IS_EQUAL(_, o)
		return
	
	# WebSocket Headers
	@Parameterized(
		{'i': 's3pPLMBiTxaQ9kYGzzhZRbK+xOo=', 'o': 's3pPLMBiTxaQ9kYGzzhZRbK+xOo='},
	)
	@Order(601)
	def testSecWebSocketAccept(self, i, o):
		_ = ParseHeader('Sec-WebSocket-Accept', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': 'permessage-deflate; client_max_window_bits', 'o': ['permessage-deflate','client_max_window_bits']},
	)
	@Order(602)
	def testSecWebSocketExtensions(self, i, o):
		_ = ParseHeader('Sec-WebSocket-Extensions', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': 'dGhlIHNhbXBsZSBub25jZQ==', 'o': 'dGhlIHNhbXBsZSBub25jZQ=='},
	)
	@Order(603)
	def testSecWebSocketKey(self, i, o):
		_ = ParseHeader('Sec-WebSocket-Key', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': 'soap, wamp', 'o': ['soap','wamp']},
		{'i': 'soap', 'o': ['soap']},
		{'i': 'wamp', 'o': ['wamp']},
	)
	@Order(604)
	def testSecWebSocketProtocol(self, i, o):
		_ = ParseHeader('Sec-WebSocket-Protocol', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': '13', 'o': '13'},
	)
	@Order(605)
	def testWebSocketVersion(self, i, o):
		_ = ParseHeader('Sec-WebSocket-Version', i)
		ASSERT_IS_EQUAL(_, o)
		return
	
	# None Classified Headers
	@Parameterized(
		{'i': 'event-source', 'o': 'event-source'},
		{'i': 'navigation-source', 'o': 'navigation-source'},
		{'i': 'trigger', 'o': 'trigger'},
	)
	@Order(901)
	def testAttributionReportingEligible(self, i, o):
		_ = ParseHeader('ATTRIBUTION_REPORTING_ELIGIBLE', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': '{"a":1,"b":"str","c":1.0}', 'o': {'a':1,'b':'str','c':1.0}},
	)
	@Order(902)
	def testAttributionReportingRegisterSource(self, i, o):
		_ = ParseHeader('ATTRIBUTION_REPORTING_REGISTER_SOURCE', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': '{"a":1,"b":"str","c":1.0}', 'o': {'a':1,'b':'str','c':1.0}},
	)
	@Order(903)
	def testAttributionReporingTrigger(self, i, o):
		_ = ParseHeader('ATTRIBUTION_REPORTING_TRIGGER', i)
		ASSERT_IS_EQUAL(_, o)
		return
