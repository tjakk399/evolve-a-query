import pytest

from decorators import repeater, sorter

def test_sorter_without_arguments():
    @sorter()
    def f():
        return [2,1,3]

    assert f() == [1,2,3]

def test_sorter_reverse():
    @sorter(reverse = True)
    def f():
        return [2,1,3]

    assert f() == [3,2,1]

def test_sorter_with_key_lambda():
    @sorter(key = lambda x: 1/x)
    def f():
        return [2,1,3]

    assert f() == [3,2,1]
