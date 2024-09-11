# -*- coding: utf-8; -*-
################################################################################
#
#  WuttaMess -- Fabric Automation Helpers
#  Copyright © 2024 Lance Edgar
#
#  This file is part of Wutta Framework.
#
#  Wutta Framework is free software: you can redistribute it and/or modify it
#  under the terms of the GNU General Public License as published by the Free
#  Software Foundation, either version 3 of the License, or (at your option) any
#  later version.
#
#  Wutta Framework is distributed in the hope that it will be useful, but
#  WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
#  FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
#  more details.
#
#  You should have received a copy of the GNU General Public License along with
#  Wutta Framework.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
APT package management
"""


def dist_upgrade(c, frontend='noninteractive'):
    """
    Run a full dist-upgrade for APT.  Essentially this runs:

    .. code-block:: sh

       apt update
       apt dist-upgrade
    """
    update(c)
    upgrade(c, dist_upgrade=True, frontend=frontend)


def install(c, *packages, **kwargs):
    """
    Install some package(s) via APT.  Essentially this runs:

    .. code-block:: sh

       apt install PKG [PKG ...]
    """
    frontend = kwargs.pop('frontend', 'noninteractive')
    packages = ' '.join(packages)
    return c.run(f'DEBIAN_FRONTEND={frontend} apt-get --assume-yes install {packages}')


def update(c):
    """
    Update the APT package lists.  Essentially this runs:

    .. code-block:: sh

       apt update
    """
    c.run('apt-get update')


def upgrade(c, dist_upgrade=False, frontend='noninteractive'):
    """
    Upgrade packages via APT.  Essentially this runs:

    .. code-block:: sh

       apt upgrade

       # ..or..

       apt dist-upgrade
    """
    options = ''
    if frontend == 'noninteractive':
        options = '--option Dpkg::Options::="--force-confdef" --option Dpkg::Options::="--force-confold"'
    upgrade = 'dist-upgrade' if dist_upgrade else 'upgrade'
    c.run(f'DEBIAN_FRONTEND={frontend} apt-get --assume-yes {options} {upgrade}')
