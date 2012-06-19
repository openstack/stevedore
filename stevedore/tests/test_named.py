from stevedore import named


def test_named():
    em = named.NamedExtensionManager(
        'stevedore.test.extension',
        ['t1'],
        invoke_on_load=True,
        invoke_args=('a',),
        invoke_kwds={'b': 'B'},
        )
    assert len(em.extensions) == 1
    assert em.names() == ['t1']
