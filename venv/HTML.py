from unittest import result


def test_add():
    result = 2 + 3
    print(f"Result is 2 + 3 = {result}")
    assert result == 5


def test_sub():
    result = 12 - 2
    print(f"Result is 12 - 2 ={result}")
    assert result == 10

def test_fail():
    result = 12 * 2
    print(f"Result is 12 * 2 = {result}")
    assert result == 10