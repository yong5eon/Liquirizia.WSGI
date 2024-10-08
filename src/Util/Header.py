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
		'ACCEPT_CHARSET': 'Accept-Charset',
		'ACCEPT_ENCODING': 'Accept-Encoding',
		'ACCEPT_LANGUAGE': 'Accept-Language',
		'ACCEPT_RANGES': 'Accept-Ranges',
		'ACCESS_CONTROL_REQUEST_METHOD': 'Access-Control-Request-Method',
		'ACCESS_CONTROL_REQUEST_HEADERS': 'Access-Control-Request-Headers',
		'ACCESS_CONTROL_REQUEST_ORIGIN': 'Access-Control-Request-Origin',
		'ACCESS_CONTROL_REQUEST_CREDENTIALS': 'Access-Control-Request-Credentials',
		'ACCESS_CONTROL_EXPOSE_HEADERS': 'Access-Control-Expose-Headers',
		'ACCESS_CONTROL_MAX_AGE': 'Access-Control-Max-Age',
		'AGE': 'Age',  # Response header
		'ALLOW': 'Allow',  # Response header
		'AUTHORIZATION': 'Authorization',
		'CACHE_CONTROL': 'Cache-Control',
		'CONNECTION': 'Connection',
		'CONTENT_ENCODING': 'Content-Encoding',
		'CONTENT_LANGUAGE': 'Content-Language',
		'CONTENT_LENGTH': 'Content-Length',
		'CONTENT_LOCATION': 'Content-Location',
		'CONTENT_MD5': 'Content-MD5',
		'CONTENT_RANGE': 'Content-Range',
		'CONTENT_TYPE': 'Content-Type',
		'COOKIE': 'Cookie',
		'DATE': 'Date',
		'ETAG': 'ETag',
		'EXPECT': 'Expect',
		'EXPIRES': 'Expires',
		'FROM': 'From',
		'HOST': 'Host',
		'IF_MATCH': 'If-Match',
		'IF_MODIFIED_SINCE': 'If-Modified-Since',
		'IF_NONE_MATCH': 'If-None-Match',
		'IF_RANGE': 'If-Range',
		'IF_UNMODIFIED_SINCE': 'If-Unmodified-Since',
		'LAST_MODIFIED': 'Last-Modified',
		'LOCATION': 'Location',
		'MAX_FORWARDS': 'Max-Forwards',
		'ORIGIN': 'Origin',
		'PRAGMA': 'Pragma',
		'PROXY_AUTHENTICATE': 'Proxy-Authenticate',
		'PROXY_AUTHORIZATION': 'Proxy-Authorization',
		'RANGE': 'Range',
		'REFERER': 'Referer',
		'RETRY_AFTER': 'Retry-After',
		'SEC_WEBSOCKET_ACCEPT': 'Sec-WebSocket-Accept',
		'SEC_WEBSOCKET_EXTENSIONS': 'Sec-WebSocket-Extensions',
		'SEC_WEBSOCKET_KEY': 'Sec-WebSocket-Key',
		'SEC_WEBSOCKET_PROTOCOL': 'Sec-WebSocket-Protocol',
		'SEC_WEBSOCKET_VERSION': 'Sec-WebSocket-Version',
		'SERVER': 'Server',
		'SERVER_PROTOCOL': 'Server-Protocol',
		'SET_COOKIE': 'Set-Cookie',
		'TE': 'TE',
		'TRAILER': 'Trailer',
		'TRANSFER_ENCODING': 'Transfer-Encoding',
		'UPGRADE': 'Upgrade',
		'USER_AGENT': 'User-Agent',
		'VARY': 'Vary',
		'VIA': 'Via',
		'WARNING': 'Warning',
		'WWW_AUTHENTICATE': 'WWW-Authenticate'
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
