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

	# Request Headers	
	# - ACCEPT_LANGUAGE: ParseAcceptLanguage()
	# - ALT_USED: ParseAltUsed()
	# - AUTHORIZATION: ParseAuthorization()
	# - COOKIE: ParseCookie()
	# - DEVICE_MEMORY: ParseFloat()
	# - DNT: ParseInteger()
	# - DOWNLINK: ParseFloat()
	# - DPR: ParseFloat()
	# - EARLY_DATA: ParseInteger()
	# - ECT: ParseString()
	# - EXPECT: ParseString()
	# - FORWARDED: ParseList(fetch=ParseParameters(sep=';'))
	# - FROM: ParseString()
	# - HOST: ParseString()
	# - IF_MATCH: ParseList()
	# - IF_MODIFIED_SINCE: ParseDate()
	# - IF_NONE_MATCH: ParseList()
	# - IF_RANGE: ParseIfRange()
	# - IF_UNMODIFIED_SINCE: ParseDate()
	# - MAX_FORWARDS: ParseInteger()
	# - ORIGIN: ParseString()
	# - PROXY_AUTHORIZATION: ParseProxyAuthorization()
	# - RANGE: ParseRange()
	# - REFERER: ParseString()
	# - RTT: ParseFloat()
	# - SAVE_DATA: ParseString()
	# - SEC_BROWSING_TOPICS: ParseString()
	# - SEC_CH_PREFERS_COLOR_SCHEME: ParseString()
	# - SEC_CH_PREFERS_REDUCED_MOTION: ParseString()
	# - SEC_CH_PREFERS_REDUCED_TRANSPARENCY: ParseString()
	# - SEC_CH_UA: ParseList()
	# - SEC_CH_UA_ARCH: ParseString()
	# - SEC_CH_UA_BITNESS: ParseInteger()
	# - SEC_CH_UA_FULL_VERSION: ParseString()
	# - SEC_CH_UA_FULL_VERSION_LIST: ParseList()
	# - SEC_CH_UA_MOBILE: ParseBoolean(true='?1')
	# - SEC_CH_UA_MODEL: ParseString()
	# - SEC_CH_UA_PLATFORM: ParseString()
	# - SEC_CH_UA_PLATFORM_VERSION: ParseString()
	# - SEC_FETCH_DEST: ParseString()
	# - SEC_FETCH_MODE: ParseString()
	# - SEC_FETCH_SITE: ParseString()
	# - SEC_FETCH_USER: ParseString()
	# - SEC_GPC: ParseBoolean(true='1')
	# - SEC_PURPOSE: ParseString()
	# - SERVICE_WORKER: ParseString()
	# - SERVICE_WORKER_NAVIGATION_PRELAOD: ParseString()
	# - TE: ParseTE()
	# - UPGRADE_INSECURE_REQUESTS: ParseBoolean(true='1')
	# - USER_AGENT: ParseString()
	# - VIEWPORT_WIDTH: ParseInteger()
	# - WIDTH: ParseInteger()
	# - X_FORWARDED_FOR: ParseList()
	# - X_FORWARDED_HOST: ParseString()
	# - X_FORWARDED_PROTO: ParseString()
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
		_ = ParseRequestHeader('Accept-Language', i)
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
		_ = ParseRequestHeader('Alt-Used', i)
		ASSERT_IS_EQUAL(_.host, o['host'])
		ASSERT_IS_EQUAL(_.port, o['port'])
		return

	@Parameterized(
		{'i': 'Basic YWxhZGRpbjpvcGVuc2VzYW1l', 'o': {'scheme': 'Basic', 'credentials': 'YWxhZGRpbjpvcGVuc2VzYW1l', 'params': {}}},
		{'i': 'Digest username="abc", password="def"', 'o': {'scheme': 'Digest', 'credentials': None, 'params': {'username':'abc','password':'def'}}},
	)
	@Order(303)
	def testAuthorization(self, i, o):
		_ = ParseRequestHeader('Authorization', i)
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
		_ = ParseRequestHeader('Cookie', i)
		for i, n in enumerate(_):
			ASSERT_IS_EQUAL(n.name, o[i]['name'])
			ASSERT_IS_EQUAL(n.value, o[i]['value'])
		return
	
	@Parameterized(
		{'i': '128', 'o': 128},
	)
	@Order(305)
	def testDeviceMemory(self, i, o):
		_ = ParseRequestHeader('Device-Memory', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': '0', 'o': 0},
		{'i': '1', 'o': 1},
	)
	@Order(306)
	def testDNT(self, i, o):
		_ = ParseRequestHeader('DNT', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': '1.7', 'o': 1.7},
	)
	@Order(307)
	def testDownlink(self, i, o):
		_ = ParseRequestHeader('Downlink', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': '2.0', 'o': 2.0},
	)
	@Order(308)
	def testDPR(self, i, o):
		_ = ParseRequestHeader('DPR', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': '1', 'o': 1},
	)
	@Order(309)
	def testEarlyData(self, i, o):
		_ = ParseRequestHeader('Early-Data', i)
		ASSERT_IS_EQUAL(_, o)
		return
	
	@Parameterized(
		{'i': '4g', 'o': '4g'},
	)
	@Order(310)
	def testECT(self, i, o):
		_ = ParseRequestHeader('ECT', i)
		ASSERT_IS_EQUAL(_, o)
		return
	
	@Parameterized(
		{'i': '100-continue', 'o': '100-continue'},
	)
	@Order(311)
	def testExpect(self, i, o):
		_ = ParseRequestHeader('Expect', i)
		ASSERT_IS_EQUAL(_, o)
		return
	
	@Parameterized(
		{'i': 'for=192.0.2.60;proto=http;by=203.0.113.43', 'o': [{'for':'192.0.2.60','proto':'http','by':'203.0.113.43'}]},
		{'i': 'for=192.0.2.43, for=198.51.100.17', 'o': [{'for':'192.0.2.43'},{'for':'198.51.100.17'}]},
	)
	@Order(312)
	def testForwarded(self, i, o):
		_ = ParseRequestHeader('Forwarded', i)
		ASSERT_IS_EQUAL(_, o)
		return
	

	@Parameterized(
		{'i': 'webmaster@example.org', 'o': 'webmaster@example.org'},
	)
	@Order(313)
	def testFrom(self, i, o):
		_ = ParseRequestHeader('From', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': 'developer.mozilla.org', 'o': 'developer.mozilla.org'},
	)
	@Order(314)
	def testHost(self, i, o):
		_ = ParseRequestHeader('Host', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': '"bfc13a64729c4290ef5b2c2730249c88ca92d82d"', 'o': ['bfc13a64729c4290ef5b2c2730249c88ca92d82d']},
		{'i': '"67ab43", "54ed21", "7892dd"', 'o': ['67ab43','54ed21','7892dd']},
		{'i': '*', 'o': ['*']},
	)
	@Order(315)
	def testIfMatch(self, i, o):
		_ = ParseRequestHeader('If-Match', i)
		ASSERT_IS_EQUAL(_, o)
		return
	
	@Parameterized(
		{'i': 'Tue, 11 Feb 2025 18:00:40 GMT', 'o': datetime.now() },
	)
	@Order(316)
	def testIfModeifiedSince(self, i, o):
		_ = ParseRequestHeader('If-Modified-Since', i)
		ASSERT_IS_EQUAL(isinstance(_, datetime), True)
		return

	@Parameterized(
		{'i': '"bfc13a64729c4290ef5b2c2730249c88ca92d82d"', 'o': ['bfc13a64729c4290ef5b2c2730249c88ca92d82d']},
		{'i': '"67ab43", "54ed21", "7892dd"', 'o': ['67ab43','54ed21','7892dd']},
		{'i': '*', 'o': ['*']},
	)
	@Order(317)
	def testIfNoneMatch(self, i, o):
		_ = ParseRequestHeader('If-None-Match', i)
		ASSERT_IS_EQUAL(_, o)
		return
	
	@Parameterized(
		{'i': 'Wed, 21 Oct 2015 07:28:00 GMT', 'o': datetime.now()},
		{'i': '"67ab43"', 'o': '67ab43'},
	)
	@Order(318)
	def testIfRange(self, i, o):
		_ = ParseRequestHeader('If-Range', i)
		if isinstance(o, str): ASSERT_IS_EQUAL(_, o)
		else: ASSERT_IS_EQUAL(isinstance(_, datetime), True)
		return
	
	@Parameterized(
		{'i': 'Tue, 11 Feb 2025 18:00:40 GMT', 'o': datetime.now() },
	)
	@Order(319)
	def testIfUnmodeifiedSince(self, i, o):
		_ = ParseRequestHeader('If-Unmodified-Since', i)
		ASSERT_IS_EQUAL(isinstance(_, datetime), True)
		return	
	
	@Parameterized(
		{'i': '4', 'o': 4},
	)
	@Order(320)
	def testMaxForwards(self, i, o):
		_ = ParseRequestHeader('Max-Forwards', i)
		ASSERT_IS_EQUAL(_, o)
		return
	
	@Parameterized(
		{'i': 'https://developer.mozilla.org', 'o': 'https://developer.mozilla.org'},
		{'i': 'https://developer.mozilla.org:80', 'o': 'https://developer.mozilla.org:80'},
	)
	@Order(321)
	def testOrigin(self, i, o):
		_ = ParseRequestHeader('Origin', i)
		ASSERT_IS_EQUAL(_, o)
		return
	
	@Parameterized(
		{'i': 'Basic YWxhZGRpbjpvcGVuc2VzYW1l', 'o': {'scheme': 'Basic', 'credentials': 'YWxhZGRpbjpvcGVuc2VzYW1l'}},
		{'i': 'Bearer kNTktNTA1My00YzLT1234', 'o': {'scheme': 'Bearer', 'credentials': 'kNTktNTA1My00YzLT1234'}},
	)
	@Order(322)
	def testProxyAuthorization(self, i, o):
		_ = ParseRequestHeader('Proxy-Authorization', i)
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
		unit, ranges = ParseRequestHeader('Range', i)
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
		_ = ParseRequestHeader('Referer', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': '125', 'o': 125},
	)
	@Order(324)
	def testRTT(self, i, o):
		_ = ParseRequestHeader('RTT', i)
		ASSERT_IS_EQUAL(_, o)
		return
	
	@Parameterized(
		{'i': 'on', 'o': 'on'},
	)
	@Order(325)
	def testSaveData(self, i, o):
		_ = ParseRequestHeader('Save-Data', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': '[{configVersion: "chrome.1", modelVersion: "1", taxonomyVersion: "1", topic: 43, version: "chrome.1:1:1"}]', 'o': '[{configVersion: "chrome.1", modelVersion: "1", taxonomyVersion: "1", topic: 43, version: "chrome.1:1:1"}]'},
	)
	@Order(326)
	def testSecBrowsingTopics(self, i, o):
		_ = ParseRequestHeader('Sec-Browsing-Topics', i)
		ASSERT_IS_EQUAL(_, o)
		return
	
	@Parameterized(
		{'i': '"dark"', 'o': 'dark'},
	)
	@Order(327)
	def testSecCHPrefersColorScheme(self, i, o):
		_ = ParseRequestHeader('Sec-CH-Prefers-Color-Scheme', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': '"reduce"', 'o': 'reduce'},
	)
	@Order(328)
	def testSecCHPefersReducedMotion(self, i, o):
		_ = ParseRequestHeader('Sec-CH-Prefers-Reduced-Motion', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': '"reduce"', 'o': 'reduce'},
	)
	@Order(329)
	def testSecCHPrefersReducedTransparency(self, i, o):
		_ = ParseRequestHeader('Sec-CH-Prefers-Reduced-Transparency', i)
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
		_ = ParseRequestHeader('Sec-CH-UA', i)
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
		_ = ParseRequestHeader('Sec-CH-UA-Arch', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': '"64"', 'o': 64},
	)
	@Order(332)
	def testSecCHUABitness(self, i, o):
		_ = ParseRequestHeader('Sec-CH-UA-Bitness', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': '"96.0.4664.110"', 'o': '96.0.4664.110'},
	)
	@Order(333)
	def testSecCHUAFullVersion(self, i, o):
		_ = ParseRequestHeader('Sec-CH-UA-Full-Version', i)
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
		_ = ParseRequestHeader('Sec-CH-UA-Full-Version-List', i)
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
		_ = ParseRequestHeader('Sec-CH-UA-Mobile', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': '"Pixel 3 XL"', 'o': 'Pixel 3 XL'},
	)
	@Order(336)
	def testSecCHUAModel(self, i, o):
		_ = ParseRequestHeader('Sec-CH-UA-Model', i)
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
		_ = ParseRequestHeader('Sec-CH-UA-Platform', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': '"10.0.0"', 'o': '10.0.0'},
	)
	@Order(338)
	def testSecCHUAPlatformVersion(self, i, o):
		_ = ParseRequestHeader('Sec-CH-UA-Platform-Version', i)
		ASSERT_IS_EQUAL(_, o)
		return
	
	@Parameterized(
		{'i': 'audio', 'o': 'audio'},
	)
	@Order(340)
	def testSecFetchDest(self, i, o):
		_ = ParseRequestHeader('Sec-Fetch-Dest', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': 'cors', 'o': 'cors'},
	)
	@Order(341)
	def testSecFetchMode(self, i, o):
		_ = ParseRequestHeader('Sec-Fetch-Mode', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': 'cross-site', 'o': 'cross-site'},
	)
	@Order(342)
	def testSetFetchSite(self, i, o):
		_ = ParseRequestHeader('Sec-Fetch-Site', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': '?1', 'o': True},
		{'i': '?0', 'o': None},
		{'i': '1', 'o': None},
	)
	@Order(343)
	def testSecFetchUser(self, i, o):
		_ = ParseRequestHeader('Sec-Fetch-User', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': '1', 'o': True},
		{'i': '0', 'o': None},
	)
	@Order(344)
	def testSecGPC(self, i, o):
		_ = ParseRequestHeader('Sec-GPC', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': 'prefetch', 'o': 'prefetch'},
	)
	@Order(345)
	def testSecPurpose(self, i, o):
		_ = ParseRequestHeader('Sec-Purpose', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': 'script', 'o': 'script'},
	)
	@Order(346)
	def testServiceWorker(self, i, o):
		_ = ParseRequestHeader('Service-Worker', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': 'true', 'o': 'true'},
		{'i': 'json_fragment1', 'o': 'json_fragment1'},
	)
	@Order(347)
	def testServiceWorkerNavigationPreload(self, i, o):
		_ = ParseRequestHeader('Service-Worker-Navigation-Preload', i)
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
		_ = ParseRequestHeader('TE', i)
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
		_ = ParseRequestHeader('Upgrade-InSecure-Requests', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0', 'o': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'},
		{'i': 'Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0', 'o': 'Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0'},
		{'i': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36', 'o': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'},
		{'i': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41', 'o': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41'},
		{'i': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59', 'o': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59'},
		{'i': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Mobile/15E148 Safari/604.1', 'o': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Mobile/15E148 Safari/604.1'},
		{'i': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)', 'o': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'},
	)
	@Order(350)
	def testUserAgent(self, i, o):
		_ = ParseRequestHeader('User-Agent', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': '343', 'o': 343},
	)
	@Order(338)
	def testViewportWidth(self, i, o):
		_ = ParseRequestHeader('Viewport-Width', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': '1024', 'o': 1024},
	)
	@Order(351)
	def testWidth(self, i, o):
		_ = ParseRequestHeader('Width', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': '203.0.113.195, 2001:db8:85a3:8d3:1319:8a2e:370:7348', 'o': ['203.0.113.195', '2001:db8:85a3:8d3:1319:8a2e:370:7348']},
		{'i': '203.0.113.195', 'o': ['203.0.113.195']},
	)
	@Order(352)
	def testXForwardedFor(self, i, o):
		_ = ParseRequestHeader('X-Forwarded-For', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': 'id42.example-cdn.com', 'o': 'id42.example-cdn.com'},
	)
	@Order(353)
	def testXForwardedHost(self, i, o):
		_ = ParseRequestHeader('X-Forwarded-Host', i)
		ASSERT_IS_EQUAL(_, o)
		return

	@Parameterized(
		{'i': 'http', 'o': 'http'},
		{'i': 'https', 'o': 'https'},
	)
	@Order(354)
	def testXForwardedProto(self, i, o):
		_ = ParseRequestHeader('X-Forwarded-Proto', i)
		ASSERT_IS_EQUAL(_, o)
		return
