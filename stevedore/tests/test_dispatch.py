from stevedore import dispatch


def test_dispatch():

    def check_dispatch(ep, *args, **kwds):
        return ep.name == 't2'

    def invoke(ep, *args, **kwds):
        return (ep.name, args, kwds)

    em = dispatch.DispatchExtensionManager(
        'stevedore.test.extension',
        lambda *args, **kwds: True,
        invoke_on_load=True,
        invoke_args=('a',),
        invoke_kwds={'b': 'B'},
    )
    assert len(em.extensions) == 2
    assert set(em.names()) == set(['t1', 't2'])

    results = em.map(check_dispatch,
                     invoke,
                     'first',
                     named='named value',
                     )
    expected = [('t2', ('first',), {'named': 'named value'})]
    assert results == expected


def test_name_dispatch():

    def invoke(ep, *args, **kwds):
        return (ep.name, args, kwds)

    em = dispatch.NameDispatchExtensionManager(
        'stevedore.test.extension',
        lambda *args, **kwds: True,
        invoke_on_load=True,
        invoke_args=('a',),
        invoke_kwds={'b': 'B'},
    )
    assert len(em.extensions) == 2
    assert set(em.names()) == set(['t1', 't2'])

    results = em.map(['t2'],
                     invoke,
                     'first',
                     named='named value',
                     )
    expected = [('t2', ('first',), {'named': 'named value'})]
    assert results == expected


def test_name_dispatch_ignore_missing():

    def invoke(ep, *args, **kwds):
        return (ep.name, args, kwds)

    em = dispatch.NameDispatchExtensionManager(
        'stevedore.test.extension',
        lambda *args, **kwds: True,
        invoke_on_load=True,
        invoke_args=('a',),
        invoke_kwds={'b': 'B'},
    )

    results = em.map(['t3', 't1'],
                     invoke,
                     'first',
                     named='named value',
                     )
    expected = [('t1', ('first',), {'named': 'named value'})]
    assert results == expected
