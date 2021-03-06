"""
Python offers two flavours of built in sets, these are sets and frozen sets.
As you can imagine, frozen sets are themselves immutable and thus hashable so can be stored inside other sets
and also used as dictionary keys.  By default, sets are mutable as we can add elements to them etc.

Note: For TLDR Notes, please reference the end of this file.
"""

# Demonstration of mutability, hashability and frozen sets as hashable keys / set elements

mutable_set = {1, 2, 3, 4}
immutable_set = frozenset([1, 2, 3, 4])

empty_set = set()
empty_set.add(mutable_set)
"""
Traceback (most recent call last):
  File "C:/workspace/learning-python/collections/set.py", line 13, in <module>
    empty_set.add(mutable_set)
TypeError: unhashable type: 'set'
"""

empty_set.add(immutable_set)
# {frozenset({1, 2, 3, 4})}

# Adding as dictionary keys:
"""
>>> mydict = {mutable_set: 'mutable!'}
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: unhashable type: 'set'
"""

# Vs frozen:

"""
>>> mydict = {immutable_set: 'immutable!'}
>>> mydict
{frozenset({1, 2, 3, 4}): 'immutable!'}
"""

------------------------------------------------------------------------------

"""
A set by definition (Set Theory) is an unordered collection of distinct, hashable elements.
The core benefits of sets in python are:
 - Extremely fast 'in' checks, 'x' in {'x', 'y', 'z'} for example
 - Remove duplicates from other collections
 - Applying various mathematically operations, such as union & intersection etc.
 
Sets out of the box support len(set), for x in set:, x in set.  Notably, sets are NOT sequences so index lookup,
slice notation and other sequence like behaviour.  Importantly sets cannot guarantee the order of elements.  Sets do 
not keep track of order of insertion, or current order of elements.  Instead they use the hash of elements to compute
where the object A) should be placed and B) should be retrieved from extremely fast. 

"""

------------------------------------------------------------------------------

"""
Sets can be constructed through two main methods, firstly using the curly braces:

>>> my_set = {1,2,3,4}
>>> type(my_set)
<class 'set'>

>>> my_set = set([1,2,3,4])
>>> type(my_set)
<class 'set'>

The core difference in these two approaches is that using the set constructor approach explicitly (set(iterable))
only accepts a single, (optional) iterable item, whereas with the braces approach, all items should be explicitly
passed in.  Note: A set CANNOT hold references to A) dictionaries and B) Lists because those two types are non hashable
due to their mutable nature.  This is shown below:

>>> my_dict = dict(a=1, b=2, c=3)
>>> new_set = {my_dict}
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: unhashable type: 'dict'

>>> my_list = [_ for _ in range(100)]
>>> my_set = set()
>>> my_set.add(my_list)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: unhashable type: 'list'

Note: Lists are an iterable, as are dictionaries (by default on keys) so this approach works just fine:

>>> immutable_list = [_ for _ in range(5)]
>>> immutable_dict = {'a': 1, 'b': 2}
>>> my_set = set(immutable_list)
>>> my_set
{0, 1, 2, 3, 4}
>>> my_set = set(immutable_dict)
>>> my_set
{'a', 'b'}

As you an see above, both of these mutable types are infact, iterables so they can be unpacked into the set.

"""

------------------------------------------------------------------------------

"""
By default as of python 3.8.5, sets are 216 bytes in size when empty.
This applies to both sets and frozen sets

>>> get_size(set())
216
>>> get_size(frozenset())
216
"""

------------------------------------------------------------------------------

"""
Python set methods [excluding dunder / private]:

>>> pprint(set_interface)
['add',
 'clear',
 'copy',
 'difference',
 'difference_update',
 'discard',
 'intersection',
 'intersection_update',
 'isdisjoint',
 'issubset',
 'issuperset',
 'pop',
 'remove',
 'symmetric_difference',
 'symmetric_difference_update',
 'union',
 'update']

"""


"""
set add(elem) function:
 - Add a new (hashable, immutable) element to the set
 - Elements cannot be added at a particular index and the set has no record of where elements are
 - If the element already exists, nothing happens
 -- args: elem (the element to be added, if element already exists nothing happens)
 -- returns: None
 -- Big O: adding to a python set is O(1) constant. note: it is possible to hit collisions (multiple) times making a 
 -- completely worst case o(n).

"""

"""
set clear() function:
 - Remove all elements from the set
 - This resizes the set accordingly as outlined below:
 
     >>> x = set([_ for _ in range(100)])
    >>> get_size(x)
    8408
    >>> x.clear()
    >>> get_size(x)
    216

-- Big O: Clearing the set is a constant operation at: O(1). similar to x = set()
 
"""


"""
set copy() function:
 - Creates a shallow copy of the set (not a deep copy!)
    >>> one = set([1,2,3,5,6,7])
    >>> two = one.copy()
    >>> from sys import getrefcount
    >>> getrefcount(one)
    2
    >>> getrefcount(two)
    2
    >>> one.add(8)
    >>> two
    {1, 2, 3, 5, 6, 7}
    >>> # vs the assignment approach
    >>>
    >>> one = set([1,2,3,4,5,6,7])
    >>> two = one
    >>> getrefcount(one)
    3
    >>> getrefcount(two)
    3
    >>> # see the same references ^
    >>> one.add(8)
    >>> one
    {1, 2, 3, 4, 5, 6, 7, 8}
    >>> # two will also have 8
    >>> two
    {1, 2, 3, 4, 5, 6, 7, 8}
    
    >>> class ShallowCopy:
...     def __init__(self, x: int) -> None:
...             self.x = x
...
    >>> one = ShallowCopy(100)
    >>> var = {one}
    >>> var2 = var.copy()
    >>> for x in var:
    ...     print(id(x))
    ...
    1623954326816
    >>> for x in var2:))
    ...     print(id(x))
    ...
    1623954326816
    
    -- Big O Notation: Due to having to iterate the set to copy, copy() is O(N), linear

"""

"""
set difference(*others) function:
set x - y function:
 - The difference() function, also implemented through the __sub__ / __rsub__ dunder method of sets returns a new
 - set with the different items from set X which do not appear in others.  This is outlined below:

 # difference() can be called without argument and in this instance, will return the set of x:
    >>> x = set([1,2,3,4,5,6])
    >>> x.difference()
    {1, 2, 3, 4, 5, 6}

    >>> other_x = set([1,3,5,7,9])
    >>> other_y = set([2,4,6,8,10])
    >>> x - other_x
    {2, 4, 6}
    >>> x - other_y
    {1, 3, 5}

    # Applying difference to multiple *others:
    >>> x = {1,2,3,4,5,6,7,8,9,10,1337}
    >>> x.difference(other_x, other_y)
    {1337}

    # Same as:
    >>> x - other_x - other_y
    {1337}

    -- Big O Notation: x.difference(y) is equivalent to O(len(x) - len(y))

"""

"""
set difference_update(*others) function:
 - Update set X to remove items in *others. 
 - note: This updates X and does not create a new set
 - note: infix operator -= is equivalent of x.difference_update(y).  This is outlined below:
 
    >>> x = set([1,2,3,4,5,6])
    >>> y = set([100,200,300,5,6])
    >>> x.difference_update(y)
    >>> x
    {1, 2, 3, 4}
    >>> z = set([1,2,3,4,5,6])
    >>> z -= y
    >>> z
    {1, 2, 3, 4}
    >>> z == x
    True
    
    # Here you can see the difference explicitly in x - y vs x-= y
    >>> x = {100, 200, 300}
    >>> y = {300, 400, 500}
    >>> z = x.copy()
    >>>
    >>>
    >>> x
    {200, 100, 300}
    >>> y
    {400, 300, 500}
    >>> z
    {200, 100, 300}
    >>> x - y
    {200, 100}
    >>> new = x - y
    >>> id(new)
    1517543477984
    >>> x -= y
    >>> id(x)
    1517543478656
"""

"""
set discard(elem) function:
 - Discards an element from the set
 - Unlike remove(elem), does NOT raise a KeyError if the elem is not present in the set
    >>> x = {1,2,3}
    >>> x.discard(4)
    >>> x.remove(4)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    KeyError: 4
 -- Big O Notation: Discarding (like removing) an element from the set is constant time O(1).
"""

"""
set intersection(*others) function:
 - Return a new set with elements common in set X and sets *others.
 - x.intersection() returns x
 - x & y is equal to x.intersection(y)
 - intersection dunder methods are: __and__, __rand__, __iand__
    >>> x = {1,2,3,4,5}
    >>> y = {6,7}
    >>> z = {3,4,5,6}
    >>>
    >>> x.intersection()
    {1, 2, 3, 4, 5}
    >>> var = x.intersection(y)
    >>> var
    set()
    >>> var = x.intersection(z)
    >>> var
    {3, 4, 5}
 - When using multiple *others, it returns a new set with elements that are in x and all of *others
 >>> x = {1,2,3,4,5}
    >>> y = {3,4,5}
    >>> z = {3,6,7}
    >>> # This should return {3} as its the only value in all 3
    >>> x & y & z
    {3}
    
 - # __and__, __rand__, __iand__ operators brief explanation:
     >>> class DunderAnd:
    ...     def __and__(self, val):
    ...             print('and')
    ...     def __rand__(self, val):
    ...             print('r-and')
    ...     def __iand__(self, val):
    ...             print('infix-and')
    ...
    >>>
    >>>
    >>> var = DunderAnd()
    >>> var & None
    'and'
    >>> None & var
    'r-and'
    >>> var &= None
    'infix-and'
 
"""

"""
set intersection_difference(*others) function:
 - Update set x keeping only elements found in it and in all of *others
 - x.intersection_difference(*others) updates x in place with elements in x AND y
 - x &= y &= z modifies x in place with items that are in x AND Y AND z
    In [9]: x = {1,2,3,4,5}
    In [10]: y = {1,2,3}
    In [11]: x.intersection_update(y)
    In [12]: x
    Out[12]: {1, 2, 3}
 
    In [13]: x = {1,2,3}
    In [14]: y = {2}
    In [15]: z = {2,3}
    In [17]: x &= y & z
    In [18]: x
    Out[18]: {2}

"""

"""
set isdisjoint(other) function:
 - x.isdisjoint(other) returns True if the x.intersection(y) would be an empty set.
 - if x has no elements in common with y, then we say x is disjoint of y
    In [19]: disjoint = {1,2,3,4,5} 
    In [20]: y = {6,7,8,9}
    In [21]: disjoint.isdisjoint(y)
    Out[21]: True
    In [22]: disjoint.isdisjoint(set())
    Out[22]: True
    In [23]: disjoint.isdisjoint({4})
    Out[23]: False
 - isdisjoint(other) accepts any type which implements the iterator protocol
    In [34]: x = {1,2,3}; y = [3,4,5]
    In [35]: x.isdisjoint(y)
    Out[35]: False
    In [36]: x = {1,3,5}; y = (5,7,9)
    In [37]: x.isdisjoint(y)
    Out[37]: False
    In [40]: x = {'d', 'o'}
    In [41]: x.isdisjoint('word')
    Out[41]: False # interesting :)
 - Attempting when a type which is not iterable is passed:
    In [42]: class A: pass 
    In [44]: x.isdisjoint(A())
    ---------------------------------------------------------------------------
    TypeError                                 Traceback (most recent call last)
    <ipython-input-44-2abc63912fb4> in <module>
    ----> 1 x.isdisjoint(A())
    
    TypeError: 'A' object is not iterable
"""

"""
set issubset(other) function:
 - Returns True if all elements of x are in y
 - x is then considered a subset of y, this is outlined below:
    In [46]: x = {1,2,3}; y = {2,3,4}
    In [47]: x.issubset(y)
    Out[47]: False
    In [48]: x = {1,2,3}; y = {1,2,3,4,5}
    In [49]: x.issubset(y)
    Out[49]: True
 - This also works with any iterable:
    In [50]: x.issubset([1,2,3,4,5,6,7])
    Out[50]: True 
 - x <= y tests if every element in x is in y
 - x < y tests for proper subsets, where every element of x is in y and x != y (see below):
    In [60]: x = {1,2,3,4,5}
    In [61]: x <= x # True
    Out[61]: True
    In [62]: x < x # False because x is equal to x
    Out[62]: False
"""

"""
set issuperset(other) function:
 - You can think of superset as the opposite of subset, every element in y is in x:
 - >= is not a 'proper' check, but confirms if all elements in y are in x
 - x > y is a 'proper' check and enforces that x is not equal to y (x != y and x >= y)
    In [65]: x = {1,2,3,4,5}
    In [66]: y = {3,4,5}
    In [67]: x >= x # True
    Out[67]: True
    In [68]: x >= x # False
    Out[68]: True
    In [69]: x >= y # True
    Out[69]: True
    In [70]: x > y # True
    Out[70]: True
    In [71]: x < y # False
    Out[71]: False
"""

"""
set pop() function:
 - Pop an item out of the set
 - As you know, sets do NOT keep track of order, so popping by index is not supported
 - Unlike other pop() counter parts, no default can be specified and KeyError if the set is empty
    In [76]: x = set('abcdefghijklmnopqrstuvwxyz')
    In [77]: x.pop()
    Out[77]: 'e'
    In [78]: x.pop()
    Out[78]: 'q'
    In [79]: x.pop()
    Out[79]: 'x'
    In [80]: x.pop()
    Out[80]: 't'
    In [81]: x
    Out[81]:
    {'a',
    'b',
    'c',
    'd',
    'f',
    'g',
    'h',
    'i',
    'j',
    'k',
    'l',
    'm',
    'n',
    'o',
    'p',
    'r',
    's',
    'u',
    'v',
    'w',
    'y',
    'z'}
 - Empty set popping:
    In [82]: x = set()
    In [83]: x.pop()
    ---------------------------------------------------------------------------
    KeyError                                  Traceback (most recent call last)
    <ipython-input-83-22e0729a7b70> in <module>
    ----> 1 x.pop()
"""

"""
set remove(elem) function:
 - removes element 'elem' from the set
 - if elem does not exist within the set, a KeyError is raised
    In [86]: from string import ascii_letters   
    In [87]: x = set(ascii_letters)
    In [88]: x.remove('0')
    ---------------------------------------------------------------------------
    KeyError                                  Traceback (most recent call last)
    <ipython-input-88-f39020323f74> in <module>
    ----> 1 x.remove('0')
    
    KeyError: '0'
"""

"""
set symmetric_difference(other) function:
 - symmetric_difference is the elements in EITHER x OR y but not in both
 - symmetric_difference is the equivalent of x ^ y
 - x.symmetric_difference(y) returns a new set, not to be confused with modifying x in-place (^=)
    In [92]: x = {1,2,3,4,5}; y = {6,7,8,9,10}
    In [93]: var = x.symmetric_difference(y)
    In [94]: var
    Out[94]: {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
 - An example of when sets are the same:
    In [95]: same_x = {1,2,3,4}; same_y = [1,2,3,4]
    In [96]: same_x.symmetric_difference(same_y)
    Out[96]: set()
 - An example with the dunder ^ operator:
    In [99]: x = {1,2,3}; y = {4,5,6}
    In [100]: var = x ^ y
    In [101]: var
    Out[101]: {1, 2, 3, 4, 5, 6}
"""

"""
set symmetric_difference_update(other) function:
 - similar to x.symmetric_difference(y) except updates set x in place.
 - returns None implicitly
 - updates x in place with elements from other which are not in x: x.symmetric_difference_update(y)
    In [23]: x = {1,2,3}
    In [24]: y = {3,4,5}
    In [25]: x.symmetric_difference_update(y)
    In [26]: x
    Out[26]: {1, 2, 4, 5}
 - Can be written using the dunder ixor implementation for multiple other sets, example below:
    In [27]: one = {1,2,3}  
    In [28]: two = {4,5,6}  
    In [29]: three = {3,6,7}  
    In [30]: one ^= two ^ three  
    In [31]: one
    Out[31]: {1, 2, 4, 5, 7}

"""

"""
set union(others*) function:
 - x.union(other) returns a new set, containing all items from both x and other
 - x.union(other) can also be written as x | other (OR)
 - Some examples are shown below:
    In [1]: x = {1,2,3,4,'hello'}
    In [2]: y = {'world', 4,3,2,1,0}
    In [3]: new = x | y
    In [4]: new
    Out[4]: {0, 1, 2, 3, 4, 'hello', 'world'}
    
 - Multiple chained unions:
    In [6]: x | {1,2,3} | {4,5,6,7}
    Out[6]: {1, 2, 3, 4, 5, 6, 7, 'hello'}
    
 - Union with multiple others:
    In [8]: a = {1,2,3}
    In [9]: b = {4,5,6}
    In [10]: c = {7,8,9}
    In [11]: a.union(b,c)
    Out[11]: {1, 2, 3, 4, 5, 6, 7, 8, 9}
"""

"""
set update(others*) function:
 - Given an iterable of others, add all elements in each iterable into the set x
 - x.update(y, z)
 - operator implementation can be used like: x |= y | z
 - Some examples of this are shown below:
 - Modifying x in place:
    In [12]: x = {1,2,3,4,5}; y = {1,2,3,4,5,6}
    In [13]: x.update(y)
    In [14]: x
    Out[14]: {1, 2, 3, 4, 5, 6}
 - Modifying x in place with multiple iterables:
    In [16]: a = {1,2,3}; b = {4,5,6}; c = {7,8,9}
    In [17]: a.update(b,c)
    In [18]: a
    Out[18]: {1, 2, 3, 4, 5, 6, 7, 8, 9}
 - Modifying x in place with multiple iterables using the operator syntax:
    In [21]: a |= set('hello') | set('world')
    In [22]: a
    Out[22]: {'d', 'e', 'h', 'l', 'o', 'r', 'w'}

"""

------------------------------------------------------------------------------


"""
Guarantee of set order cannot be assured.  Sets by default are length 8 in size, after filling to a certain percentage
the order in which.  Here we can see the set resizing when the 5th element is added:

    >>> x = set()
    >>> get_size(x)
    216
    >>> x.add(1)
    >>> x.add(2)
    >>> x.add(3)
    >>> x.add(4)
    >>> get_size(x)
    216
    >>> pprint(x)
    {1, 2, 3, 4}
    # Still 216 bytes until we add one more:

    >>> x.add(5)
    >>> get_size(x)
    728  # Finally resized! Note this resizing looks to approximately 3.37~ %

    We can see that the order of the iterable is not guaranteed within sets in python:
    some_list = [1,2,20,210,6,100]
    >>> some_list = [1,2,20,210,6,100]
    >>> set(some_list)
    {1, 2, 100, 6, 210, 20} # not the same as the sequenced list

"""

------------------------------------------------------------------------------

"""
frozen set vs set functions & public interface:

# using sets to remove duplicates! :)

difference = set(dir(set()).difference(set(dir(frozenset())))

    >>> print(difference)
    {'__iand__',
     '__ior__',
     '__isub__',
     '__ixor__',
     'add',
     'clear',
     'difference_update',
     'discard',
     'intersection_update',
     'pop',
     'remove',
     'symmetric_difference_update',
     'update'}
     
     # As we can see above, frozen sets being immutable they cannot modify the set after creation!
     # It is still possible for things like x.difference(y) where x is type: frozenset
     # However, note the __isub__ dunder difference, x -= y (surprisingly?) does actually work... but it returns
     # a new frozenset under such circumstances.
     # This is because when dunder __isub__ is not implemented on an object, the dunder __sub__ is a fallback
     
     >>> class Augment:
    ...     def __sub__(self, other):
    ...             print('dunder sub')
    ...     def __isub__(self, other):
    ...             print('dunder isub')
    ...
    ...
    >>> var = Augment()
    >>> var - None
    'dunder sub'
    >>> var -= None
    'dunder isub'
    
    >>> class NoAugment:
    ...     def __sub__(self, other):
    ...             print('normal dunder sub...')
    ...
    ...
    >>> var = NoAugment()
    >>> var -= None
    'normal dunder sub...'
    
     # Here we can see, frozenset class does NOT have an implementation of dunder isub:
     >>> print(dir(frozenset()))
    ['__and__',
     '__class__',
     '__contains__',
     '__delattr__',
     '__dir__',
     '__doc__',
     '__eq__',
     '__format__',
     '__ge__',
     '__getattribute__',
     '__gt__',
     '__hash__',
     '__init__',
     '__init_subclass__',
     '__iter__',
     '__le__',
     '__len__',
     '__lt__',
     '__ne__',
     '__new__',
     '__or__',
     '__rand__',
     '__reduce__',
     '__reduce_ex__',
     '__repr__',
     '__ror__',
     '__rsub__',
     '__rxor__',
     '__setattr__',
     '__sizeof__',
     '__str__',
     '__sub__',
     '__subclasshook__',
     '__xor__',
     'copy',
     'difference',
     'intersection',
     'isdisjoint',
     'issubset',
     'issuperset',
     'symmetric_difference',
     'union']
     
     # and set() does:
     >>> print(dir(set()))
    ['__and__',
     '__class__',
     '__contains__',
     '__delattr__',
     '__dir__',
     '__doc__',
     '__eq__',
     '__format__',
     '__ge__',
     '__getattribute__',
     '__gt__',
     '__hash__',
     '__iand__',
     '__init__',
     '__init_subclass__',
     '__ior__',
     '__isub__',
     '__iter__',
     '__ixor__',
     '__le__',
     '__len__',
     '__lt__',
     '__ne__',
     '__new__',
     '__or__',
     '__rand__',
     '__reduce__',
     '__reduce_ex__',
     '__repr__',
     '__ror__',
     '__rsub__',
     '__rxor__',
     '__setattr__',
     '__sizeof__',
     '__str__',
     '__sub__',
     '__subclasshook__',
     '__xor__',
     'add',
     'clear',
     'copy',
     'difference',
     'difference_update',
     'discard',
     'intersection',
     'intersection_update',
     'isdisjoint',
     'issubset',
     'issuperset',
     'pop',
     'remove',
     'symmetric_difference',
     'symmetric_difference_update',
     'union',
     'update']
     
     So when we ask a frozen set to perform -= it actually falls back to performing x - y and returns a new frozenset.
     
"""

------------------------------------------------------------------------------


"""
TLDR Notes:
# Stores hashable, immutable, unordered elements
# Two types of built in set (set() / frozenset())
# Create sets using set(iterable), frozenset(iterable), {n,...}
# By default, empty braces will create a dictionary (care) = {} # Type Dict, not an empty set!
# By default, python sets are allocated sizing for 8 elements. 
# By default, resizing occurs when the set is 66%~ (TODO FIX THIS) full? seems to resize 3.5x its size?
# Sets cannot guarantee the order of elements, resizing etc can shift the order completely
# Comparison of sets, cares not about order of elements - only the elements within explicitly.
# set.difference() returns a set with the elements from x that are not in *others
# set.difference() is equivalent to using '-' (x - y - z) and this is due to a dunder __sub__ implementation
# set.intersection() returns a set with the elements from x that are also in *others
# set.intersection() is equivalent to using '&' (x & y & z) and this is due to a dunder __and__ implementation
# set.intersection_update(*others) can also be written x &= y & z where x is now items in x AND y AND z
# non-operator methods of union, difference, intersection, symmetric_difference, issubset, issuperset will accept any iterable
"""