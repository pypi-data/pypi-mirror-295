r"""
>>> import bz2, gzip, fileinput
>>> bzf = getfixture('tmpdir') / 'data.bz2'
>>> bzf.write_binary(bz2.compress(b'Foo\nBar\nBiz'))
>>> gzf = getfixture('tmpdir') / 'data.gz'
>>> gzf.write_binary(gzip.compress(b'Bang\nBuz'))
>>> plain = getfixture('tmpdir') / 'data.txt'
>>> plain.write_text('Flam', encoding='utf-8')
>>> files = map(str, [bzf, gzf, plain])
>>> for line in fileinput.FileInput(files, openhook=hook_compressed, **_encoding):
...      print(line.strip())
Foo
Bar
Biz
Bang
Buz
Flam

"""

import io
import os
import sys


_encoding = dict((('encoding', 'utf-8'),) * bool(sys.version_info > (3, 10)))


def hook_compressed(filename, mode, *, encoding=None, errors=None):
    ext = os.path.splitext(filename)[1]
    if ext == '.gz':
        import gzip

        stream = gzip.open(filename, mode)
    elif ext == '.bz2':
        import bz2

        stream = bz2.BZ2File(filename, mode)
    else:
        return open(filename, mode, encoding=encoding, errors=errors)

    # gzip and bz2 are binary mode by default.
    if "b" not in mode:
        stream = io.TextIOWrapper(stream, encoding=encoding, errors=errors)
    return stream
