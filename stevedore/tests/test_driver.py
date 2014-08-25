"""Tests for stevedore.extension
"""

import mock
import pkg_resources

from stevedore import driver
from stevedore.tests import test_extension
from stevedore.tests import utils


class TestCallback(utils.TestCase):
    def test_detect_plugins(self):
        em = driver.DriverManager('stevedore.test.extension', 't1')
        names = sorted(em.names())
        self.assertEqual(names, ['t1'])

    def test_call(self):
        def invoke(ext, *args, **kwds):
            return (ext.name, args, kwds)
        em = driver.DriverManager('stevedore.test.extension', 't1')
        result = em(invoke, 'a', b='C')
        self.assertEqual(result, ('t1', ('a',), {'b': 'C'}))

    def test_driver_property_not_invoked_on_load(self):
        em = driver.DriverManager('stevedore.test.extension', 't1',
                                  invoke_on_load=False)
        d = em.driver
        self.assertIs(d, test_extension.FauxExtension)

    def test_driver_property_invoked_on_load(self):
        em = driver.DriverManager('stevedore.test.extension', 't1',
                                  invoke_on_load=True)
        d = em.driver
        self.assertIsInstance(d, test_extension.FauxExtension)

    def test_no_drivers(self):
        try:
            driver.DriverManager('stevedore.test.extension.none', 't1')
        except RuntimeError as err:
            self.assertIn("No 'stevedore.test.extension.none' driver found",
                          str(err))

    def test_bad_driver(self):
        try:
            driver.DriverManager('stevedore.test.extension', 'e2')
        except ImportError:
            pass
        else:
            self.assertEquals(False, "No error raised")

    def test_multiple_drivers(self):
        # The idea for this test was contributed by clayg:
        # https://gist.github.com/clayg/6311348
        fep_name = 'stevedore.extension.ExtensionManager._find_entry_points'
        with mock.patch(fep_name) as fep:
            fep.return_value = [
                pkg_resources.EntryPoint.parse('backend = pkg1:driver'),
                pkg_resources.EntryPoint.parse('backend = pkg2:driver'),
            ]
            for ep in fep.return_value:
                ep.load = lambda *args, **kwds: 'pkg backend'
            try:
                driver.DriverManager('stevedore.test.multiple_drivers',
                                     'backend')
            except RuntimeError as err:
                self.assertIn("Multiple", str(err))
            fep.assert_called_with('stevedore.test.multiple_drivers')
