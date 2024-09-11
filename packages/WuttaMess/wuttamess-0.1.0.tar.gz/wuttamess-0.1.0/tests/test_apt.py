# -*- coding: utf-8; -*-

from unittest import TestCase
from unittest.mock import patch, MagicMock

from wuttamess import apt as mod


class TestDistUpgrade(TestCase):

    def test_basic(self):
        c = MagicMock()
        with patch.object(mod, 'update') as update:
            with patch.object(mod, 'upgrade') as upgrade:
                mod.dist_upgrade(c, frontend='whatever')
                update.assert_called_once_with(c)
                upgrade.assert_called_once_with(c, dist_upgrade=True, frontend='whatever')


class TestInstall(TestCase):

    def test_basic(self):
        c = MagicMock()
        mod.install(c, 'postfix')
        c.run.assert_called_once_with('DEBIAN_FRONTEND=noninteractive apt-get --assume-yes install postfix')


class TestUpdate(TestCase):

    def test_basic(self):
        c = MagicMock()
        mod.update(c)
        c.run.assert_called_once_with('apt-get update')


class TestUpgrade(TestCase):

    def test_basic(self):
        c = MagicMock()
        mod.upgrade(c)
        c.run.assert_called_once_with('DEBIAN_FRONTEND=noninteractive apt-get --assume-yes --option Dpkg::Options::="--force-confdef" --option Dpkg::Options::="--force-confold" upgrade')
