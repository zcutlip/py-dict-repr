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
