__all__ = ['app']

from ._run import _run

def app(appname, applescript, background=False):
    """execute applescript `tell application "VLC" ...`"""
    cmd = """tell app "%s"
    %s
end tell
""" % (appname, applescript)
    return _run(cmd,background)
