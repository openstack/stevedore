from mock import Mock

from stevedore import enabled
from stevedore.tests.test_test_manager import (test_extension, test_extension2,
                                               excluded, unwanted)


def test_enabled():
    def check_enabled(ep):
        return ep.name == 't2'
    em = enabled.EnabledExtensionManager(
        'stevedore.test.extension',
        check_enabled,
        invoke_on_load=True,
        invoke_args=('a',),
        invoke_kwds={'b': 'B'},
    )
    assert len(em.extensions) == 1
    assert em.names() == ['t2']


def test_enabled_after_load():
    def check_enabled(ext):
        return ext.obj and ext.name == 't2'
    em = enabled.EnabledExtensionManager(
        'stevedore.test.extension',
        check_enabled,
        invoke_on_load=True,
        invoke_args=('a',),
        invoke_kwds={'b': 'B'},
    )
    assert len(em.extensions) == 1
    assert em.names() == ['t2']


def test_enabled_manager_should_check_all_extensions():
    check_func = Mock()

    enabled.EnabledExtensionManager.make_test_instance([excluded,
                                                        test_extension,
                                                        unwanted,
                                                        test_extension2],
                                                       check_func)

    check_func.assert_any_call(test_extension)
    check_func.assert_any_call(test_extension2)
    check_func.assert_any_call(excluded)
    check_func.assert_any_call(unwanted)


def test_enabled_manager_should_include_only_passing_extensions():
    def underscore_checker(extension):
        return '_' in extension.name

    em = enabled.EnabledExtensionManager.make_test_instance([excluded,
                                                             test_extension,
                                                             unwanted,
                                                             test_extension2],
                                                            underscore_checker)

    extensions = list(em)

    assert test_extension in extensions
    assert test_extension2 in extensions

    assert excluded not in extensions
    assert unwanted not in extensions
