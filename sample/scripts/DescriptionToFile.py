# -*- coding: utf-8 -*-

from Liquirizia.WSGI.Description import (
	Descriptor, 
	Information,
	Contact,
)
from Liquirizia.Serializer import SerializerHelper

from json import dump, dumps

_ = Descriptor(
	info=Information(
		title='Liquirizia.WSGI Sample API',
		version='0.1.0',
		summary='Sample API Document',
		description='Sample API',
		contact=Contact(
			name='Heo Yongseon',
			url='https://github.com/yong5eon/Liquirizia.WSGI',
			email='contact@email.com'
		)
	)
)

_.load(path='sample/api')

with open('sample.json', 'wb') as f:
	text = SerializerHelper.Serialize(_.toDocument(), 'application/json')
	f.write(text.encode('utf-8'))

