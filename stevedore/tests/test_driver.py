"""Tests for stevedore.extension
"""

from stevedore import driver


def test_detect_plugins():
    em = driver.DriverManager('stevedore.test.extension', 't1')
    names = sorted(em.names())
    assert names == ['t1']


def test_call():
    def invoke(ext, *args, **kwds):
        return (ext.name, args, kwds)
    em = driver.DriverManager('stevedore.test.extension', 't1')
    result = em(invoke, 'a', b='C')
    assert result == ('t1', ('a',), {'b': 'C'})


def test_no_drivers():
    try:
        driver.DriverManager('stevedore.test.extension.none', 't1')
    except RuntimeError as err:
        assert "No 'stevedore.test.extension.none' driver found" == str(err)
