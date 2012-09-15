"""Tests for stevedore.extension
"""

from stevedore import driver
from stevedore.tests import test_extension


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


def test_driver_property_not_invoked_on_load():
    em = driver.DriverManager('stevedore.test.extension', 't1',
                              invoke_on_load=False)
    d = em.driver
    assert d is test_extension.FauxExtension


def test_driver_property_invoked_on_load():
    em = driver.DriverManager('stevedore.test.extension', 't1',
                              invoke_on_load=True)
    d = em.driver
    assert isinstance(d, test_extension.FauxExtension)


def test_no_drivers():
    try:
        driver.DriverManager('stevedore.test.extension.none', 't1')
    except RuntimeError as err:
        assert "No 'stevedore.test.extension.none' driver found" in str(err)
