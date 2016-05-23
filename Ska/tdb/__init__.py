from .tdb import *


def test(*args, **kwargs):
    import os
    import pytest
    pkg_path = os.path.dirname(__file__)
    os.chdir(pkg_path)
    pytest.main(list(args), **kwargs)
