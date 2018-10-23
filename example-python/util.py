

import heapq

class PriorityQueue(object):
    def __init__(self, f=lambda x: x):
        self.A = []
        self.f = f

    def append(self, item):
       heapq.heappush(self.A, (self.f(item), item)) 

    def extend(self, items):
        for i in items:
            self.append(i)

    def pop(self):
        return heapq.heappop(self.A)[1]

    def __len__(self):
        return len(self.A)

    def __str__(self):
        return str(self.A)

    def __contains__(self, item):
        return any(x==item for _, x in self.A)

def memoize(fn):
    """Memoize fn: make it remember the computed value for any argument list"""
    def memoized_fn(*args):
        if not memoized_fn.cache.has_key(args):
            memoized_fn.cache[args] = fn(*args)
        return memoized_fn.cache[args]
    memoized_fn.cache = {}
    return memoized_fn

def update(x, **entries):
    """Update a dict; or an object with slots; according to entries.
    >>> update({'a': 1}, a=10, b=20)
    {'a': 10, 'b': 20}
    >>> update(Struct(a=1), a=10, b=20)
    Struct(a=10, b=20)
    """
    if isinstance(x, dict):
        x.update(entries)
    else:
        x.__dict__.update(entries)
    return x
