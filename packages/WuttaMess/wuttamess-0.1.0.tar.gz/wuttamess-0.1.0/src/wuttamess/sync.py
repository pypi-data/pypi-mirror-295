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
Synchronize Files

See :doc:`/narr/usage` for a basic example.
"""

import fabsync


def make_root(path, dest='/'):
    """
    Make and return a "root" object for use with future sync calls.

    This is a convenience wrapper around
    :func:`fabsync:fabsync.load()`.

    :param path: Path to local file tree.  Usually this is relative to
       the ``fabfile.py`` location, otherwise should be absolute.

    :param dest: Path for target file tree.
    """
    return fabsync.load(path, dest)


def isync(c, root, selector=None, echo=True, **kwargs):
    """
    Sync files, yielding the result for each as it goes.

    This is a convenience wrapper around
    :func:`fabsync:fabsync.isync()`.

    :param c: Connection object.

    :param root: File tree "root" object as obtained from
       :func:`make_root()`.

    :param selector: This can be a simple "subpath" string, indicating
       a section of the file tree.  For instance: ``'etc/postfix'``

    :param echo: Flag indicating whether the path for each file synced
       should be echoed to stdout.  Generally thought to be useful but
       may be disabled.

    :param \**kwargs: Any remaining kwargs are passed as-is to
       :func:`fabsync:fabsync.isync()`.
    """
    if selector:
        if not isinstance(selector, fabsync.ItemSelector):
            selector = fabsync.ItemSelector.new(selector)
        kwargs['selector'] = selector

    for result in fabsync.isync(c, root, **kwargs):
        if echo:
            print(f"{result.path}{' [modified]' if result.modified else ''}")
        yield result


def check_isync(c, root, selector=None, **kwargs):
    """
    Sync all files and return boolean indicating whether any actual
    modifications were made.

    Arguments are the same as for :func:`isync()`, which this calls.

    :returns: ``True`` if any sync result indicates a file was
       modified; otherwise ``False``.
    """
    return any([result.modified
                for result in isync(c, root, selector, **kwargs)])
