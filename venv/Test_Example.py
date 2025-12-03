import pytest

def test_pass():
    assert True

def test_fail():
    assert False

def test_skip():
    pytest.skip("skipping this test")
