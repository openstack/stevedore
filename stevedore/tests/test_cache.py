#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.

"""Tests for stevedore._cache"""

import json
import os
import sys
import tempfile

from unittest import mock

from stevedore import _cache
from stevedore.tests import utils


class TestCache(utils.TestCase):
    def test_disable_caching_executable(self):
        """Test caching is disabled if python interpreter is located under /tmp
        directory (Ansible)
        """
        with mock.patch.object(sys, 'executable', '/tmp/fake'):
            sot = _cache.Cache()
            self.assertTrue(sot._disable_caching)

    def test_disable_caching_file(self):
        """Test caching is disabled if .disable file is present in target
        dir
        """
        cache_dir = _cache._get_cache_dir()

        with mock.patch('os.path.isfile') as mock_path:
            mock_path.return_value = True
            sot = _cache.Cache()
            mock_path.assert_called_with(f'{cache_dir}/.disable')
            self.assertTrue(sot._disable_caching)

            mock_path.return_value = False
            sot = _cache.Cache()
            self.assertFalse(sot._disable_caching)

    @mock.patch('os.makedirs')
    @mock.patch('builtins.open')
    def test__get_data_for_path_no_write(self, mock_open, mock_mkdir):
        sot = _cache.Cache()
        sot._disable_caching = True
        mock_open.side_effect = IOError
        sot._get_data_for_path(('fake',))
        mock_mkdir.assert_not_called()

    def test__get_data_for_path_write(self):
        with tempfile.TemporaryDirectory() as cache_dir:
            sot = _cache.Cache(cache_dir=cache_dir)
            data = sot._get_data_for_path(('fake',))
            digest, _ = _cache._hash_settings_for_path(('fake',))
            # only the cache file is left behind, no temporary file
            self.assertEqual([digest], os.listdir(cache_dir))
            with open(os.path.join(cache_dir, digest)) as f:
                self.assertEqual(json.loads(json.dumps(data)), json.load(f))

    def test__get_data_for_path_replace_invalid(self):
        with tempfile.TemporaryDirectory() as cache_dir:
            digest, _ = _cache._hash_settings_for_path(('fake',))
            filename = os.path.join(cache_dir, digest)
            with open(filename, 'w') as f:
                f.write('{"groups": {"x": [["a", "b"')
            sot = _cache.Cache(cache_dir=cache_dir)
            data = sot._get_data_for_path(('fake',))
            self.assertEqual([digest], os.listdir(cache_dir))
            with open(filename) as f:
                self.assertEqual(json.loads(json.dumps(data)), json.load(f))

    def test__write_cache_file_error(self):
        with tempfile.TemporaryDirectory() as cache_dir:
            filename = os.path.join(cache_dir, 'cache')
            with open(filename, 'w') as f:
                f.write('old')
            with mock.patch.object(json, 'dump', side_effect=ValueError):
                self.assertRaises(
                    ValueError,
                    _cache._write_cache_file,
                    filename,
                    _cache._build_cacheable_data(),
                )
            # the existing file is untouched and no temporary file is left
            self.assertEqual(['cache'], os.listdir(cache_dir))
            with open(filename) as f:
                self.assertEqual('old', f.read())

    def test__build_cacheable_data(self):
        # this is a rubbish test as we don't actually do anything with the
        # data, but it's too hard to script since it's totally environmentally
        # dependent and mocking out the underlying calls would remove the value
        # of this test (we want to test those underlying API calls)
        ret = _cache._build_cacheable_data()
        self.assertIsInstance(ret['groups'], dict)
