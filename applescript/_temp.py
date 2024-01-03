import os
from tempfile import mkstemp


def _tempfile():
    f, path = mkstemp()
    os.close(f)
    return path
