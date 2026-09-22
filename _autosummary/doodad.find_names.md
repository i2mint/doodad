# doodad.find_names

### doodad.find_names(src, \*, value_normalizer=<function dflt_value_normalizer>)

Finds all the names (variables, functions, etc.) in a piece of code or data.

```pycon
>>> mapping = {'c': 1, 'b': {'a': 2, 'd': 3}}
>>> list(find_names(mapping))
['c', 'b', 'a', 'd']
```

It also works on a python object whose source code `inspect.getsource` can
retrieve – a function defined in an importable module, for instance:

```pycon
>>> from doodad.find_names import yield_names_from_mapping
>>> names = list(find_names(yield_names_from_mapping))
>>> 'yield_names_from_mapping' in names and 'mapping' in names
True
```
