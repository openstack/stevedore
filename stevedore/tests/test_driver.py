"""Tests for stevedore.extension
"""

from stevedore import driver


def test_detect_plugins():
    em = driver.DriverManager('stevedore.test.extension', 't1')
    names = sorted(em.names())
    assert names == ['t1']


def test_no_drivers():
    try:
        driver.DriverManager('stevedore.test.extension.none', 't1')
    except RuntimeError as err:
        assert "No 'stevedore.test.extension.none' driver found" == str(err)
