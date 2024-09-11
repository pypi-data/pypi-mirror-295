# -*- coding: utf-8; -*-

from pathlib import Path
from unittest import TestCase
from unittest.mock import patch, MagicMock

from fabsync import SyncedRoot, ItemSelector

from wuttamess import sync as mod


class TestMakeRoot(TestCase):

    def test_basic(self):
        root = mod.make_root('files')
        self.assertIsInstance(root, SyncedRoot)
        self.assertEqual(root.src, Path('files'))
        self.assertEqual(root.dest, Path('/'))


class TestIsync(TestCase):

    def test_basic(self):
        c = MagicMock()
        root = mod.make_root('files')
        with patch.object(mod, 'fabsync') as fabsync:
            fabsync.ItemSelector = ItemSelector

            # nothing to sync
            fabsync.isync.return_value = []
            results = list(mod.isync(c, root))
            self.assertEqual(results, [])
            fabsync.isync.assert_called_once_with(c, root)

            # sync one file
            fabsync.isync.reset_mock()
            result = MagicMock(path='/foo', modified=True)
            fabsync.isync.return_value = [result]
            results = list(mod.isync(c, root))
            self.assertEqual(results, [result])
            fabsync.isync.assert_called_once_with(c, root)

            # sync with selector
            fabsync.isync.reset_mock()
            result = MagicMock(path='/foo', modified=True)
            fabsync.isync.return_value = [result]
            results = list(mod.isync(c, root, 'foo'))
            self.assertEqual(results, [result])
            fabsync.isync.assert_called_once_with(c, root, selector=fabsync.ItemSelector.new('foo'))


class TestCheckIsync(TestCase):

    def test_basic(self):
        c = MagicMock()
        root = mod.make_root('files')
        with patch.object(mod, 'isync') as isync:

            # file(s) modified
            result = MagicMock(path='/foo', modified=True)
            isync.return_value = [result]
            self.assertTrue(mod.check_isync(c, root))

            # not modified
            result = MagicMock(path='/foo', modified=False)
            isync.return_value = [result]
            self.assertFalse(mod.check_isync(c, root))
