"""
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from ..lists import inlist



def test_inlist() -> None:
    """
    Perform various tests associated with relevant routines.
    """

    needle = 123

    haystack = [123, 456]

    assert inlist(needle, haystack)
