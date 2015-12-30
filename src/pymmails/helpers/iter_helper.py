"""
@file
@brief Helpers with iterator
"""


def iterator_prev_next(iter):
    """
    iterator on a sequence and returns another iterator with
    ``previous item, current item, next item``,

    @param      iter        iterator
    @return                 iterator

    the previous item is ``None`` at the beginning of the sequence,
    the next item is the same at the end of the sequence
    """
    prev, item, next = None, None, None
    notempty = False
    for current in iter:
        notempty = True
        prev = item
        item = next
        next = current
        if item is not None:
            yield prev, item, next
    if notempty:
        prev = item
        item = next
        next = None
        yield prev, item, next
