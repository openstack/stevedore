"""Tests for failure loading callback
"""
from testtools.matchers import GreaterThan
import mock

from stevedore import extension
from stevedore import named
from stevedore.tests import utils


class TestCallback(utils.TestCase):
    def test_extension_failure_custom_callback(self):
        errors = []

        def failure_callback(manager, entrypoint, error):
            errors.append((manager, entrypoint, error))

        em = extension.ExtensionManager('stevedore.test.extension',
                                        invoke_on_load=True,
                                        on_load_failure_callback=
                                        failure_callback)
        extensions = list(em.extensions)
        self.assertThat(len(extensions), GreaterThan(0))
        self.assertEqual(len(errors), 2)
        for manager, entrypoint, error in errors:
            self.assertIs(manager, em)
            self.assertIsInstance(error, (IOError, ImportError))

    @mock.patch('stevedore.named.NamedExtensionManager._load_plugins')
    def test_missing_entrypoints_callback(self, load_fn):
        errors = set()

        def callback(names):
            errors.update(names)

        load_fn.return_value = [
            extension.Extension('foo', None, None, None)
        ]
        named.NamedExtensionManager('stevedore.test.extension',
                                    names=['foo', 'bar'],
                                    invoke_on_load=True,
                                    on_missing_entrypoints_callback=callback)
        self.assertEqual(errors, {'bar'})
