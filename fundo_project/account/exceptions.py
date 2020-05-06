class UsernameAlreadyExistsError(Exception):
    def __init__(self,msg,code):
        self.code = code
        self.msg = msg

class EmailAlreadyExistsError(Exception):
    def __init__(self,msg,code):
        self.code = code
        self.msg = msg

class PasswordDidntMatched(Exception):
    def __init__(self,msg,code):
        self.code = code
        self.msg = msg

class PasswordPatternMatchError(Exception):
    def __init__(self,msg,code):
        self.code = code
        self.msg = msg