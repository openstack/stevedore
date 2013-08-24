from mock import Mock
from nose.tools import raises
from stevedore import (ExtensionManager, NamedExtensionManager, HookManager,
                       EnabledExtensionManager, DriverManager)
from stevedore.extension import Extension


test_extension = Extension('test_extension', None, None, None)
test_extension2 = Extension('another_one', None, None, None)
excluded = Extension('excluded', None, None, None)
unwanted = Extension('unwanted', None, None, None)


def test_extension_name_should_be_listed():
    em = ExtensionManager.make_test_instance([test_extension])

    assert test_extension.name in em.names()


def test_iterator_should_yield_extension():
    em = ExtensionManager.make_test_instance([test_extension])

    assert test_extension == next(iter(em))


def test_manager_should_allow_name_access():
    em = ExtensionManager.make_test_instance([test_extension])

    assert test_extension == em[test_extension.name]


def test_manager_should_call():
    em = ExtensionManager.make_test_instance([test_extension])
    func = Mock()

    em.map(func)

    func.assert_called_once_with(test_extension)


def test_manager_should_call_all():
    em = ExtensionManager.make_test_instance([test_extension2,
                                              test_extension])
    func = Mock()

    em.map(func)

    func.assert_any_call(test_extension2)
    func.assert_any_call(test_extension)


def test_manager_return_values():
    def mapped(ext, *args, **kwds):
        return ext.name

    em = ExtensionManager.make_test_instance([test_extension2,
                                              test_extension])
    results = em.map(mapped)
    assert sorted(results) == ['another_one', 'test_extension']


def test_manager_should_eat_exceptions():
    em = ExtensionManager.make_test_instance([test_extension])

    func = Mock(side_effect=RuntimeError('hard coded error'))

    results = em.map(func, 1, 2, a='A', b='B')
    assert results == []


@raises(RuntimeError)
def test_manager_should_propagate_exceptions():
    em = ExtensionManager.make_test_instance([test_extension],
                                             propagate_map_exceptions=True)
    func = Mock(side_effect=RuntimeError('hard coded error'))

    em.map(func, 1, 2, a='A', b='B')


def test_named_manager_should_include_named_extensions():
    em = NamedExtensionManager.make_test_instance([excluded,
                                                   test_extension,
                                                   unwanted,
                                                   test_extension2],
                                                  ['test_extension',
                                                   'another_one'])

    extensions = list(em)

    assert test_extension in extensions
    assert test_extension2 in extensions


def test_named_manager_should_not_include_unnamed_extensions():
    em = NamedExtensionManager.make_test_instance([excluded,
                                                   test_extension,
                                                   unwanted,
                                                   test_extension2],
                                                  ['test_extension',
                                                   'another_one'])

    extensions = list(em)

    assert excluded not in extensions
    assert unwanted not in extensions


def test_hook_manager_should_return_named_extensions():
    hook1 = Extension('captain', None, None, None)
    hook2 = Extension('captain', None, None, None)

    em = HookManager.make_test_instance([hook1, hook2], 'captain')

    assert [hook1, hook2] == em['captain']


def test_hook_manager_should_not_include_unnamed_extensions():
    em = HookManager.make_test_instance([excluded, test_extension,
                                         unwanted, test_extension2],
                                        'test_extension')

    extensions = em['test_extension']

    assert test_extension2 not in extensions
    assert excluded not in extensions
    assert unwanted not in extensions
