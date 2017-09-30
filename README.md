## python-most-common
Python script for calculating occurrences of words, verbs or function names in .py files in specified location.

#### Usage
Just run most_common.py with python interpreter and with desired command/arguments.

##### Commands:
- words
```bash
$ pyhton most_common.py words --path /tmp/my-scripts --top 4
```
- verbs
```bash
$ pyhton most_common.py verbs --path /tmp/my-scripts
```
- functions
```bash
$ pyhton most_common.py functions
```

##### Arguments:
- Path for parsing: `--path` When not specified, current working directory is used.
- Number of values in resulting set: `--top` If absent, full set will be returned.

##### Output: 
[('path', 18), ('names', 14), ('name', 14), ('tree', 12)]
