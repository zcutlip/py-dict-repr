# Python Dictionary Representation

## Description

The `DictRepr` class is an abstract base class that enables any subclass to define its own dictionary representation. This makes it possible to do:

```python
dict_repr = dict(arbitrary_object)
```

The subclass only needs to do two things:

- Override the `keys()` instance method to return a list of strings
- Have the keys map to variables or properties on that object

## Example

```python
lass MyArbitraryClass(DictRepr):

    _keys = ["uppercase", "length"]

    def __init__(self, value: str):
        self._value = value

    @property
    def uppercase(self):
        return self._value.upper()

    @property
    def length(self):
        return len(self._value)

    def keys(self):
        return self._keys


if __name__ == "__main__":
    myobj = MyArbitraryClass("Hello World")
    mydict = dict(myobj)
    print("mydict type: {}".format(type(mydict)))
    pprint(mydict)
```

```console
$ python3 examples/dict_repr_example.py
mydict type: <class 'dict'>
{'length': 11, 'uppercase': 'HELLO WORLD'}
```

## Mapping Keys to Object Attributes

It may be the case that a desired dicitonary key isn't the name of the corresponding attribute. For example, a string may have spaces or other characters that, while perfectly suitable as a dictionary key, make it illegal as an object attribute name.

In this case, the `KeyTuple` class provides a mapping between key string and attribute name. Simply include a KeyTuple object in place of the key string:

```Python
_keys = [
    KeyTuple("string with spaces 1", "no_spaces_1"),
    KeyTuple("string with spaces 2", "no_spaces_2")
]
```

### KeyTuple Example

Let's modify the previous example:


```python
from py_dict_repr import DictRepr, KeyTuple
class MyArbitraryClass(DictRepr):

    _keys = [
        KeyTuple("uppercase verion", "uppercase"),
        KeyTuple("string length", "length"),
        # KeyTuple may be mixed with regular key strings
        "lowercase"
    ]

    def __init__(self, value: str):
        self._value = value

    @property
    def uppercase(self):
        return self._value.upper()

    @property
    def lowercase(self):
        return self._value.lower()

    @property
    def length(self):
        return len(self._value)

    def keys(self):
        return self._keys


if __name__ == "__main__":
    myobj = MyArbitraryClass("Hello World")
    mydict = dict(myobj)
    print("mydict type: {}".format(type(mydict)))
    pprint(mydict)
```

```console
$ python3 examples/dict_repr_example.py
python3 ./examples/dict_repr_keytuple_example.py
mydict type: <class 'dict'>
{string length: 11, uppercase verion: 'HELLO WORLD', 'lowercase': 'hello world'}
```

