import itertools

def nonempty(iterator):
    """Check the next element on the iterator. If there is no next element, throw; otherwise return
    an iterator that doesn't consume the first element."""
    return itertools.chain([next(iterator)], iterator)

def partition(iterable, condition):
    """Partition the given iterable into sub-iterables against the given condition.
       Example: partition(iterable, lambda x: x != '\n')
       - Partitions the iterable (of strings) on blank lines"""
    delegate = iter(iterable)
    while True:
        try:
            yield nonempty(itertools.takewhile(condition, delegate))
        except StopIteration:
            return