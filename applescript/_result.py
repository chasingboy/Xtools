
class Result:
    code = None
    out = None
    err = None

    def __init__(self,code,out,err):
        self.code = code
        self.out = out.decode("utf-8").rstrip()
        self.err = err.decode("utf-8").rstrip()
