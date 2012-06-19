"""Tests for stevedore.extension
"""

from stevedore import extension


class FauxExtension(object):
    def __init__(self, name, *args, **kwds):
        self.name = name
        self.args = args
        self.kwds = kwds


def test_detect_plugins():
    em = extension.ExtensionManager('stevedore.test.extension')
    names = sorted(em.names())
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
