# -*- coding: utf-8 -*-

from urllib.parse import parse_qs

__all__ = (
	'ToHeaderName',
	'ParseHeader',
	'ParseRange',
)


def ToHeaderName(key):
	return {
		'ACCEPT': 'Accept',
		'ACCEPT_CH': 'Accept-CH',
		'ACCEPT_CHARSET': 'Accept-Charset',
		'ACCEPT_ENCODING': 'Accept-Encoding',
		'ACCEPT_LANGUAGE': 'Accept-Language',
		'ACCEPT_PATCH': 'Accept-Patch',
		'ACCEPT_POST': 'Accept-POST',
		'ACCEPT_RANGES': 'Accept-Ranges',
		'ACCESS_CONTROL_ALLOW_CREDENTIALS': 'Access-Control-Allow-Credentials',
		'ACCESS_CONTROL_ALLOW_HEADERS': 'Access-Control-Allow-Headers',
		'ACCESS_CONTROL_ALLOW_METHODS': 'Access-Control-Allow-Methods',
		'ACCESS_CONTROL_ALLOW_ORIGIN': 'Access-Control-Allow-Origin',
		'ACCESS_CONTROL_EXPOSE_HEADERS': 'Access-Control-Expose-Headers',
		'ACCESS_CONTROL_MAX_AGE': 'Access-Control-Max-Age',
		'ACCESS_CONTROL_REQUEST_HEADERS': 'Access-Control-Request-Headers',
		'ACCESS_CONTROL_REQUEST_METHOD': 'Access-Control-Request-Method',
		'AGE': 'Age',
		'ALLOW': 'Allow',
		'ALT_SVC': 'Alt-Svc',
		'ALT_USED': 'Alt-Used',
		'AUTHORIZATION': 'Authorization',
		'CACHE_CONTROL': 'Cache-Control',
		'CLEAR_SITE_DATA': 'Clear-Site-Data',
		'CONNECTION': 'Connection',
		'CONTENT_DIGEST': 'Content-Digest',
		'CONTENT_DISPOSITION': 'Content-Disposition',
		'CONTENT_DPR': 'Content-DPR',
		'CONTENT_ENCODING': 'Content-Encoding',
		'CONTENT_LANGUAGE': 'Content-Language',
		'CONTENT_LENGTH': 'Content-Length',
		'CONTENT_LOCATION': 'Content-Location',
		'CONTENT_MD5': 'Content-MD5',
		'CONTENT_RANGE': 'Content-Range',
		'CONTENT_TYPE': 'Content-Type',
		'COOKIE': 'Cookie',
		'CROSS_ORIGIN_EMBEDDER_POLICY': 'Cross-Origin-Embedder-Policy',
		'CROSS_ORIGIN_OPENER_POLICY': 'Cross-Origin-Opener-Policy',
		'CROSS_ORIGIN_RESOURCE_POLICY': 'Cross-Origin-Resource-Policy',
		'DATE': 'Date',
		'DEVICE_MEMORY': 'Device-Memory',
		'ETAG': 'ETag',
		'EXPECT': 'Expect',
		'EXPECT_CT': 'Expect-CT',
		'EXPIRES': 'Expires',
		'Forwarded': 'Forwarded',
		'FROM': 'From',
		'HOST': 'Host',
		'IF_MATCH': 'If-Match',
		'IF_MODIFIED_SINCE': 'If-Modified-Since',
		'IF_NONE_MATCH': 'If-None-Match',
		'IF_RANGE': 'If-Range',
		'IF_UNMODIFIED_SINCE': 'If-UnmodiFromfied-Since',
		'KEEP_ALIVE': 'Keep-Alive',
		'LAST_MODIFIED': 'Last-Modified',
		'LINK': 'Link',
		'LOCATION': 'Location',
		'MAX_FORWARDS': 'Max-Forwards',
		'ORIGIN': 'Origin',
		'PRAGMA': 'Pragma',
		'PRIORITY': 'Priority',
		'PROXY_AUTHENTICATE': 'Proxy-Authenticate',
		'PROXY_AUTHORIZATION': 'Proxy-Authorization',
		'RANGE': 'Range',
		'REFERER': 'Referer',
		'REFERRER_POLICY': 'Referrer-Policy',
		'REFRESH': 'Refresh',
		'REPORT_TO': 'Report-To',
		'REPR_DIGEST': 'Repr-Digest',
		'RETRY_AFTER': 'Retry-After',
		'SEC_FETCH_DEST': 'Sec-Fetch-Dest',
		'SEC_FETCH_MODE': 'Sec-Fetch-Mode',
		'SEC_FETCH_SITE': 'Sec-Fetch-Site',
		'SEC_FETCH_USER': 'Sec-Fetch-User',
		'SEC_PURPOSE': 'Sec-Purpose',
		'SEC_WEBSOCKET_ACCEPT': 'Sec-WebSocket-Accept',
		'SEC_WEBSOCKET_EXTENSIONS': 'Sec-WebSocket-Extensions',
		'SEC_WEBSOCKET_KEY': 'Sec-WebSocket-Key',
		'SEC_WEBSOCKET_PROTOCOL': 'Sec-WebSocket-Protocol',
		'SEC_WEBSOCKET_VERSION': 'Sec-WebSocket-Version',
		'SERVER': 'Server',
		'SERVER_PROTOCOL': 'Server-Protocol',
		'SERVER_TIMING': 'Server-Timing',
		'SERVICE_WORKER_NAVIGATION_PRELOAD': 'Service-Worker-Navigation-Preload',
		'SET_COOKIE': 'Set-Cookie',
		'SOURCEMAP': 'SourceMap',
		'STRICT_TRANSPORT_SECURITY': 'Strict-Transport-Security',
		'TE': 'TE',
		'TIMING_ALLOW_ORIGIN': 'Timing-Allow-Origin',
		'TRAILER': 'Trailer',
		'TRANSFER_ENCODING': 'Transfer-Encoding',
		'UPGRADE': 'Upgrade',
		'UPGRADE_INSECURE_REQUESTS': 'Upgrade-Insecure-Requests',
		'USER_AGENT': 'User-Agent',
		'VARY': 'Vary',
		'VIA': 'Via',
		'WANT_CONTENT_DIGEST': 'Want-Content-Digest',
		'WANT_DIGEST': 'Want-Digest',
		'WANT_REPR_DIGEST': 'Want-Repr-Digest',
		'WARNING': 'Warning',
		'WIDTH': 'Width',
		'WWW_AUTHENTICATE': 'WWW-Authenticate',
		'X_CONTENT_TYPE_OPTION': 'X-Content-Type-Option',
		'X_DNS_PREFETCH_CONTROL': 'X-DNS-Prefetch-Control',
		'X_FORWARDED_FOR': 'X-Forwarded-For',
		'X_FORWARDED_HOST': 'X-Forwarded-Host',
		'X_FORWARDED_PROTO': 'X-Forwarded-Proto',
		'X_FORWARDED_PROTOCOL': 'X-Forwarded-Protocol',
		'X_XSS_PROTECTION': 'X-XSS-Protection',
	}.get(key.upper().replace('-', '_'), key)


def ParseHeader(v: str):
	vs = []
	args = v.split(',')
	for arg in args:
		v, *qs = arg.split(';', 1)
		if len(qs):
			qs = parse_qs(qs[0].strip())
		else:
			qs = None
		vs.append((v, qs))
	return {
		'expr': v,
		'args': vs
	}

def ParseRange(range, maxlen=0):
	"""
	Yield (start, end) ranges parsed from a HTTP Range header. Skip
	unsatisfiable ranges. The end index is non-inclusive.
	"""
	if range[:6] != 'bytes=':
		return

	ranges = [r.split('-', 1) for r in range[6:].split(',') if '-' in r]

	for offset, end in ranges:
		try:
			if not offset:  # bytes=-100 : last 100 bytes
				offset, end = max(0, maxlen - int(end)), maxlen
			elif not end:  # bytes=100- : all but the first 99 bytes
				offset, end = int(offset), maxlen
			else:  # bytes=100-200 : bytes 100-200 (inclusive)
				offset, end = int(offset), min(int(end) + 1, maxlen)
			if 0 <= offset < end <= maxlen:
				yield offset, end
		except ValueError:
			pass
