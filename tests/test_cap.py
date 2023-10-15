import os
import sys


def test_ggg():
    ff = f'PYTHONPATH: {os.environ.get("PYTHONPATH", "Not set")}'
    ddd = f"System Path: {sys.path}"

    assert True
