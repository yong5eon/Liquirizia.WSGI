# Documentation with OAS(OpenAPI Specficiations)

## Description to OAS(OPenAPI Specifications) Document

```python
from Liquirizia.WSGI.Description import Descriptor, Information, Contact
from json import dumps

_ = Descriptor(info=Information(
  title='${TITLE}',
  version='${VERSION}',
  summary='${SUMMARY}',
  description='${DESCRIPTION}',
  contact=Contact(
    name='${CONTACT_NAME}',
    url='${CONTACT_URL}',
    email='${CONTACT_EMAIL}'
  )
))
text = dumps(_.toDocument())
```

## Apply Swagger

### Install swagger-ui-py

```shell
> pip install swagger-ui-py
```

### Add Handler to swager-ui-py

#### Docuement Handler

```python
from Liquirizia.FileSystemObject import Helper as FileSystemObjectHelper
from Liquirizia.FileSystemObject.Implements.FileSystem import (
  Configuration as FileSystemObjectConfiguration, 
  Connection as FileSystemObject,
)
from Liquirizia.WSGI.Properties import RequestRunner
from Liquirizia.WSGI.Request import Request
from Liquirizia.WSGI import Response

from swagger_ui.core import ApplicationDocument

from collections.abc import Mapping
from json import dumps

def handler(doc: ApplicationDocument):

  class GetAPIDocument(RequestRunner):
    def __init__(self, request: Request):
      self.request = request
      return
    def run(self):
      return Response(
        status=200,
        message='OK',
        body=doc.doc_html.encode('utf-8'),
        format='text/html',
        charset='utf-8',
      )
  doc.app.add(
    object=GetAPIDocument,
    method='GET',
    url=doc.url_prefix,
  )

  class GetAPIConfig(RequestRunner):
    def __init__(self, request: Request):
      self.request = request
      return
    def run(self):
      def encoder(o):
        if isinstance(o, Mapping): return dict(o)
        return o
      return Response(
        status=200,
        message='OK',
        body=dumps(
          doc.get_config(self.request.header('Host')),
          default=encoder
        ).encode('utf-8'), 
        format='application/json',
        charset='utf-8',
      )
  doc.app.add(object=GetAPIConfig, method='GET', url=doc.swagger_json_uri_absolute)
  FileSystemObjectHelper.Set(
    'DocumentResource',
    FileSystemObject,
    FileSystemObjectConfiguration(doc.static_dir)
  )
  doc.app.addFileSystemObject(
    FileSystemObjectHelper.Get('DocumentResource'),
    doc.static_uri_absolute, 
  )
  return

def match(doc: ApplicationDocument):
  try:
    from Liquirizia.WSGI import Application
    if isinstance(doc.app, Application):
      return handler
  except ImportError:
    pass
  return None
```

#### Import DocumentHandler

```python
import sys
import DocumentHandler

from swagger_ui import supported_list

sys.modules['swagger_ui.handlers.Liquirizia'] = DocumentHandler
supported_list.append('Liquirizia')
```

### Add swagger-ui-py to Application

```python
from Liquirizia.WSGI import Application, Configuration, Router
from Liquirizia.WSGI.Description import (
	Descriptor,
  Information,
  Contact,
)

...

from swagger_ui import api_doc

aps = Application()

...

api_doc(
  aps,
  config=Descriptor().toDocument(),
  url_prefix='${URL}',
  title='${TITLE}',
)
```

## 참고

- [OpenAPI Specifications](https://swagger.io/specification)
- [JSON Schema Documents](https://json-schema.org/docs)
