"""Tests for stevedore.extension
"""

from stevedore import extension


class FauxExtension(object):
    def __init__(self, *args, **kwds):
        self.args = args
        self.kwds = kwds


def test_detect_plugins():
    em = extension.ExtensionManager('stevedore.test.extension')
    names = sorted(em.names())
    assert names == ['t1', 't2']


def test_iterable():
    em = extension.ExtensionManager('stevedore.test.extension')
    names = sorted(e.name for e in em)
    assert names == ['t1', 't2']


def test_invoke_on_load():
    em = extension.ExtensionManager('stevedore.test.extension',
                                    invoke_on_load=True,
                                    invoke_args=('a',),
                                    invoke_kwds={'b': 'B'},
                                    )
    assert len(em.extensions) == 2
    for e in em.extensions:
        assert e.obj.args == ('a',)
        assert e.obj.kwds == {'b': 'B'}


def test_map_return_values():
    def mapped(ext, *args, **kwds):
        return ext.name

    em = extension.ExtensionManager('stevedore.test.extension',
                                    invoke_on_load=True,
                                    )
    results = em.map(mapped)
    assert sorted(results) == ['t1', 't2']


def test_map_arguments():
    objs = []

    def mapped(ext, *args, **kwds):
        objs.append((ext, args, kwds))

    em = extension.ExtensionManager('stevedore.test.extension',
                                    invoke_on_load=True,
                                    )
    em.map(mapped, 1, 2, a='A', b='B')
    assert len(objs) == 2
    names = sorted([o[0].name for o in objs])
    assert names == ['t1', 't2']
    for o in objs:
        assert o[1] == (1, 2)
        assert o[2] == {'a': 'A', 'b': 'B'}


def test_map_eats_errors():

    def mapped(ext, *args, **kwds):
        raise RuntimeError('hard coded error')

    em = extension.ExtensionManager('stevedore.test.extension',
                                    invoke_on_load=True,
                                    )
    results = em.map(mapped, 1, 2, a='A', b='B')
    assert results == []


def test_map_errors_when_no_plugins():

    def mapped(ext, *args, **kwds):
        pass

    em = extension.ExtensionManager('stevedore.test.extension.none',
                                    invoke_on_load=True,
                                    )
    try:
        em.map(mapped, 1, 2, a='A', b='B')
    except RuntimeError as err:
        assert 'No stevedore.test.extension.none extensions found' == str(err)
