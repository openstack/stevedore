"""Tests for stevedore.extension
"""
from mock import Mock, sentinel
from nose.tools import raises

import mock
import pkg_resources

from stevedore import driver
from stevedore.extension import Extension
from stevedore.tests import test_extension


mock_entry_point = Mock(module_name='test.extension', attrs=['obj'])
a_driver = Extension('test_driver', mock_entry_point, sentinel.driver_plugin,
                     sentinel.driver_obj)


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


def test_multiple_drivers():
    # The idea for this test was contributed by clayg:
    # https://gist.github.com/clayg/6311348
    fep_name = 'stevedore.extension.ExtensionManager._find_entry_points'
    with mock.patch(fep_name) as fep:
        fep.return_value = [
            pkg_resources.EntryPoint.parse('backend = pkg1:driver'),
            pkg_resources.EntryPoint.parse('backend = pkg2:driver'),
        ]
        for ep in fep.return_value:
            ep.load = lambda: 'pkg backend'
        try:
            driver.DriverManager('stevedore.test.multiple_drivers', 'backend')
        except RuntimeError as err:
            assert "Multiple" in str(err), str(err)
        fep.assert_called_with('stevedore.test.multiple_drivers')


@raises(RuntimeError)
def test_instance_driver_not_found_should_raise():
    extension = Extension('a_driver', None, None, None)
    driver.DriverManager.make_test_instance(
        [extension], 'this_is_not_the_driver_you_are_looking_for')


@raises(RuntimeError)
def test_instance_multiple_drivers_found_should_raise():
    extension = Extension('test_driver', mock_entry_point, None, None)
    copycat = Extension('test_driver', mock_entry_point, None, None)

    driver.DriverManager.make_test_instance([extension, copycat],
                                            'test_driver')


def test_instance_should_find_named_driver():
    em = driver.DriverManager.make_test_instance([a_driver], 'test_driver')
    assert ['test_driver'] == em.names()


def test_instance_call():
    def invoke(ext, *args, **kwds):
        return (ext.name, args, kwds)
    em = driver.DriverManager.make_test_instance([a_driver], 'test_driver')
    result = em(invoke, 'a', b='C')
    assert result == ('test_driver', ('a',), {'b': 'C'})


def test_instance_driver():
    em = driver.DriverManager.make_test_instance([a_driver], 'test_driver')
    assert sentinel.driver_obj == em.driver
