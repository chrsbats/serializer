
import snappy
import msgpack
import msgpack_numpy as m
m.patch()
import gzip
import json
import numpy as np

class MyNumpyJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, np.generic):
            return np.asscalar(obj)
        else:
            return super(MyNumpyJsonEncoder, self).default(obj)

class SnappyMsgpackEncoder:

    def dumps(self,x):
        return snappy.compress(msgpack.packb(x))
    def loads(self,x_enc):
        return msgpack.unpackb(snappy.uncompress(x_enc), encoding = "utf-8")

class MsgpackEncoder:
    def dumps(self,x):
        return msgpack.packb(x)
    def loads(self,x_enc):
        return msgpack.unpackb(x_enc, encoding = "utf-8")

class GzipMsgpackEncoder:
    def dumps(self,x):
        return gzip.compress(msgpack.packb(x))
    def loads(self,x_enc):
        return msgpack.unpackb(gzip.decompress(x_enc), encoding = "utf-8")

class JsonEncoder:
    def dumps(self,x):
        return json.dumps(x, cls=MyNumpyJsonEncoder)
    def loads(self,x_enc):
        return json.loads(x_enc, encoding = "utf-8")

class GzipJsonEncoder:
    def dumps(self,x):
        return gzip.compress(bytes(json.dumps(x,  cls=MyNumpyJsonEncoder), encoding = 'utf-8'))
    def loads(self,x_enc):
        return json.loads(gzip.decompress(x_enc), encoding = "utf-8")
