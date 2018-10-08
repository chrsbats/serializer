from encoders import SnappyMsgpackEncoder, MsgpackEncoder, JsonEncoder, GzipJsonEncoder, GzipMsgpackEncoder

class_registry = {}
encoder_registry = {}

#Binary with very fast compression.
encoder_registry['snappy-msgpack'] = SnappyMsgpackEncoder()
#Well known binary data format.
encoder_registry['msgpack'] = MsgpackEncoder()
#Text format used just about everywhere.  Human readable.
encoder_registry['json'] = JsonEncoder()
#Json with standard web compression
encoder_registry['gzip-json'] = GzipJsonEncoder()
#Smaller than snappy but a bit slower to uncompress.  There is a trade off here dependent on network bandwidth.
encoder_registry['gzip-msgpack'] = GzipMsgpackEncoder()

def dumps(x,encoder='snappy-msgpack'):
    if hasattr(x,'__serialized__'):
        s = x.__dict__
        working = {}
        for k,v in s.items():
            if hasattr(v,'__serialized__'):
                working[k] = dumps(v)
            else:
                working[k] = v
        s = working
        cls = x.__class__
        s['__serialized__'] = cls.__module__ + '.' + cls.__name__
        return encoder_registry[encoder].dumps(s)
    else:
        return encoder_registry[encoder].dumps(x)

def loads(x_enc,encoder='snappy-msgpack'):
    x = encoder_registry[encoder].loads(x_enc)
    if isinstance(x,dict):
        working = {}
        for k, v in x.items():
            if isinstance(v,dict):
                if '__serialized__' in v:
                    working[k] = loads(v)
                else:
                    working[k] = v
            else:
                working[k] = v
        x = working
        if '__serialized__' in x:
            object = class_registry[x['__serialized__']].__new__(class_registry[x['__serialized__']])
            object.__dict__ = x
            return object
    return x

def load(self,f,encoder='snappy-msgpack'):
    return loads(f.read(),encoder)

def dump(self,x,f,encoder='snappy-msgpack'):
    f.write(self.dumps(x),encoder)

#class decorator
def serialized(cls):
    global class_registry
    if not hasattr(cls, "__serialized__"):
        cls.__serialized__ = True
    class_registry[cls.__module__ + '.' + cls.__name__] = cls
    return cls


class Format:

    def __init__(self,encoding):
        self.encoding = encoding

    def dump(self,x,f):
        return dump(x,f,self.encoding)

    def dumps(self,x):
        return dumps(x,self.encoding)

    def load(self,x):
        return load(x,self.encoding)

    def loads(self,x):
        return loads(x,self.encoding)

json = Format('json')
gzip_json = Format('gzip-json')
json_gzip = Format('gzip-json')
msgpack = Format('msgpack')
snappy_msgpack = Format('snappy-msgpack')
gzip_msgpack = Format('gzip-msgpack')
