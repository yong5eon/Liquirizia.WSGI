# 파일 및 파일 시스템 서빙

## 파일 서빙

```python
from Liquirizia.WSGI import Application

...

aps = Application(
	...
)

aps.addFile('/path/to', '${URI}')
aps.addFiles('/path/to', '${URI_PREFIX}')
```

## 파일 시스템 서빙

```python
from Liquirizia.WSGI import Application

from Liquirizia.FileSystemObject import Helper as FileSystemObjectHelper
from Liquirizia.FileSystemObject.Implements.FileSystem import (
		Configuration as FileSystemObjectConfiguration, 
		Connection as FileSystemObject,
)

...

aps = Application(
	...
)

FileSystemObjectHelper.Set(
	'${FILE_SYSTEM}',
	FileSystemObject,
	FileSystemObjectConfiguration('/path/to')
)

aps.addFileSystemObject(
	FileSystemObjectHelper.Get('${FILE_SYSTEM}'),
	prefix='${URI_PREFIX}',
	...
)
```
