# Bats' serializer

Some utilities for serializing python objects in a safe and efficient manner.

serialize.py has methods for safe, compressed, numpy aware, binary / json serialization with basic object support.
By default the encoding is snappy compressed msgpack but also supports json and gzip.
The default encoding supports numpy arrarys via the msgpack-numpy lib.
Passing a numpy array to the json serializer will turn the array into lists of regular numbers for human readable consumption.
Classes must be registered with the @serialized decorator in order for them to be supported.

Use:

```python
import numpy as np
from serialize import serialized, json, snappy_msgpack

@serialized
class Example:
    def __init__(self,a=2):
        self.z = np.ones(a)

x = Example(4)

y = snappy_msgpack.dumps(x)
z = snappy_msgpack.loads(y)

print(z.z)
print(type(z.z))

y = json.dumps(x)
z = json.loads(y)

print(z.z)
print(type(z.z))

"""
outputs:
[1. 1. 1. 1.]
<class 'numpy.ndarray'>
[1.0, 1.0, 1.0, 1.0]
<class 'list'>
"""
```
