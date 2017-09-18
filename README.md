## python-most-common
Python script for calculating occurrences of words, verbs or function names in .py files

#### Usage
```python
from most_common import get_top_words_in_path

top_words = get_top_words_in_path('/Users/user/project', top_size=5)
print(top_words)

>>>[('path', 18), ('names', 14), ('name', 14), ('tree', 12)]
 
```