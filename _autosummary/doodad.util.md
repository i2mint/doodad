# doodad.util

Utils for doodad.

### Functions

| [`mk_str_attr_obj`](#doodad.util.mk_str_attr_obj)(iterable[, name, trans])   | Make an object with given string attributes.                                          |
|---------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------|
| [`target_instance_checker`](#doodad.util.target_instance_checker)(\*target_types)    | Returns a function that checks if an object is an instance of any of the target_types |

### doodad.util.mk_str_attr_obj(iterable, name=None, trans=None)

Make an object with given string attributes.

The purpose of this function is to offer a different option to having to write
strings in code when specifying a string value when this value should only be
taken from a fixed set of values, and use tab completion to see the available
values.

* **Parameters:**
  * **iterable** ([`Iterable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Iterable)) – an iterable of strings (or a space separate string)
  * **name** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – the name of the namedtuple

```pycon
>>> f = mk_str_attr_obj('date worker offre success')
>>> f.date
'date'
>>> f.worker
'worker'
>>> f.does_not_exist
Traceback (most recent call last):
...
AttributeError: 'AttrObj' object has no attribute 'does_not_exist'
```

`f` is a `namedtuple` so you can do things like:

```pycon
>>> list(f)
['date', 'worker', 'offre', 'success']
>>> date, worker, offer, success = f
>>> offer
'offre'
```

### doodad.util.target_instance_checker(\*target_types)

Returns a function that checks if an object is an instance of any of the target_types
