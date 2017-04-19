import  uuid, functools, threading, logging, time

#数据库引擎对象：
class _Engine(object):
    def __init__(self,connect):
        self._connect=connect
    def connect(self):
        return self._connect

engine=None


# 持有数据库连接的上下文对象:
class _DbCtx(threading.local):
    def __init__(self):
        self.connect=None
        self.transction=0
    def is_init(self):
        return not self.connect is None
    def init(self):
        self.connect=_LasyConnection()
        self.transction=0
    def cleanup(self):
        self.connect.cleanup()
        self.connect=None
    def cursor(self):
        return self.connect.cursor()
_db_ctx=_DbCtx()



class _LasyConnection(object):

    def __init__(self):
        self.connection = None

    def cursor(self):
        if self.connection is None:
            connection = engine.connect()
            logging.info('open connection <%s>...' % hex(id(connection)))
            self.connection = connection
        return self.connection.cursor()

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()

    def cleanup(self):
        if self.connection:
            connection = self.connection
            self.connection = None
            logging.info('close connection <%s>...' % hex(id(connection)))
            connection.close()

#ORM
class Dict(dict):
    def __init__(self,names=(),values=(),**kw):
        super(Dict,self).__init__(**kw)
        for k,v in zip(names,values):
            self[k]=v

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"dict has no attribute '%s'" %key)
    def __setattr__(self, key, value):
        self[key]=value

def next_id(t=None):
    if t is None:
        t=time.time()
    return '%015d%s000' % (int(t * 1000), uuid.uuid4().hex)

