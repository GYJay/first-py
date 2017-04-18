class _Engine(object):
    def __init__(self,connect):
        self._connect=connect
    def connect(self):
        return self._connect

engine=None