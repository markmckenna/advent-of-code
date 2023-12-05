import itertools

def nonempty(iterator):
    """Check the next element on the iterator. If there is no next element, throw; otherwise return
    an iterator that doesn't consume the first element."""
    return itertools.chain([next(iterator)], iterator)

def partition(iterable, condition):
    delegate = iter(iterable)
    while True:
        try:
            yield nonempty(itertools.takewhile(condition, delegate))
        except StopIteration:
            return