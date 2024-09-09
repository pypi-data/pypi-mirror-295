from simpleworkspace.__lazyimporter__ import __LazyImporter__, __TYPE_CHECKING__
if(__TYPE_CHECKING__):
    from . import csvreader as _csvreader
    from . import logreader as _logreader
    from . import m3u8reader as _m3u8reader
    from . import archive as _archive

csvreader: '_csvreader' = __LazyImporter__(__package__, '.csvreader')
m3u8reader: '_m3u8reader' = __LazyImporter__(__package__, '.m3u8reader')
logreader: '_logreader' = __LazyImporter__(__package__, '.logreader')
archive: '_archive' = __LazyImporter__(__package__, '.archive')
