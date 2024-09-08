"""
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Any
from typing import Sequence



def inlist(
    needle: Any,  # noqa: ANN401
    haystack: Sequence[Any],
) -> bool:
    """
    Return the boolean indicating whether needle in haystack.

    Example
    -------
    >>> haystack = [1, 2, 3]
    >>> inlist(2, haystack)
    True

    :param needle: Provided item that may be within haystack.
    :param haystack: List of items which may contain needle.
    :returns: Boolean indicating whether needle in haystack.
    """

    return needle in haystack
