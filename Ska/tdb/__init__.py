from .tdb import *


def test(*args):
    """Run self tests"""
    import pytest
    pytest.main(list(args))
