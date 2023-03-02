class FatalException(Exception):

    def __int__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg
