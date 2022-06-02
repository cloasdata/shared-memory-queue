# shared-memory-deque
## readme
StaticQueue class memes the collections.deque interface.
The goal for this class was to improve performance of mp.Queue class.

Outcome:
shared-memory-deque is slower than the classic mp.Queue.
The supplied implementation is limited to static size per item and bytes only.
Pickling is not included and needs to be done in front.
So I dropped the idea and did not finalize. 
One clear advantage is the pickle-ability of shared-memory-deque. So it can be easily 
invoked anywhere without the need to inherit from the process spwan/fork.

## install
```pip install shared-memory-deque```

## usage
```python
from shared_memory_deque import StaticDeque
deque = StaticDeque(10, 2)
deque.append(b"ed")
deque.pop()
```

## bottle neck
I found that the memoryview assignment of large chunk size is the most time-consuming.
~~A possible workaround could to have a second data object which is build counter-wise.
so that one could do a pop_left as a pop from a reversed(data)~~
Another solution could be to just ignore the leading bytes until the memory chunk is consumed 
with data. When put then a new block is created and assigned. One could use a first pointer. 


```commandline
Function: pop_left at line 72

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    72                                               def pop_left(self):
    73     10000     441134.0     44.1      6.3          if not self.is_empty:
    74     10000     228660.0     22.9      3.3              res = self.data.buf[:self.length].tobytes()
    75     10000    5496619.0    549.7     78.8              self.data.buf[:self._memsize - self.length] = self.data.buf[self.length:self._memsize]
    76     10000     754754.0     75.5     10.8              self.last = self.last - self.length
    77     10000      53957.0      5.4      0.8              return res
    78                                                   else:
    79                                                       raise Empty

```

## __future__
Not sure if I will add more free time to this little project. 
So don't use this module for production or anything else half ways serious. 
