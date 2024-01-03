import os
import subprocess

from ._result import Result
from ._temp import _tempfile

def _run(script, background=False, javascript=False):
    """run script file/string"""
    if not background:
        args = ["osascript", "-l", "JavaScript", "-"] if javascript else ["osascript", "-"]
        kwargs = dict(stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    else:
        f = script if os.path.exists(script) else _tempfile()
        if not os.path.exists(script):
            open(f,'w').write(script)
        args = ["osascript", "-l", "JavaScript", f] if javascript else ["osascript", f]
        kwargs = {'stdout':open(os.devnull, 'wb'),'stderr':open(os.devnull, 'wb')}
    proc = subprocess.Popen(args,**kwargs)
    if not background:
        cmd = open(script).read() if os.path.exists(script) else script
        out, err = proc.communicate(input=cmd.encode("utf-8"))
        return Result(proc.returncode,out, err)
