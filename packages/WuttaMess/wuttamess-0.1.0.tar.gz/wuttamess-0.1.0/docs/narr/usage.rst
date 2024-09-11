
Usage
=====

The expected use case is as follows:

Let's say you have a Linux machine "myserver" and you want to setup
these software systems on it:

* `Postfix <https://www.postfix.org/>`_
* `PostgreSQL <https://www.postgresql.org/>`_
* `collectd <https://www.collectd.org/>`_

Create a folder to contain the ``fabfile.py`` etc.  Let's also assume
you will have other machines to setup, and you want to commit all this
to source control.

Recommended project structure is like:

.. code-block:: none

   myproject
   └── machines
       └── myserver
           ├── fabfile.py
           ├── files
           │   └── etc
           │       ├── collectd
           │       │   └── collectd.conf
           │       └── postfix
           │           └── main.cf
           └── Vagrantfile

More details on these below.


.. _fabfile-example:

``fabfile.py``
--------------

This is a "typical" fabfile, to the extent there is such a thing.
This file contains Fabric "tasks" which may be executed on the target
machine via SSH.  For more on that concept see
:ref:`invoke:defining-and-running-task-functions`.

In this example we define "bootstrap" tasks for the setup, but that is
merely a personal convention.  You can define tasks however you need::

   """
   Fabric script for myserver
   """

   from fabric import task
   from wuttamess import apt, sync


   # nb. this is used below, for file sync
   root = sync.make_root('files')


   @task
   def bootstrap_all(c):
       """
       Bootstrap all aspects of the server
       """
       bootstrap_base(c)
       bootstrap_postgresql(c)
       bootstrap_collectd(c)


   @task
   def bootstrap_base(c):
       """
       Bootstrap the base system
       """
       apt.dist_upgrade(c)

       # postfix
       apt.install(c, 'postfix')
       if sync.check_isync(c, root, 'etc/postfix'):
           c.run('systemctl restart postfix')


   @task
   def bootstrap_postgresql(c):
       """
       Bootstrap the PostgreSQL service
       """
       apt.install(c, 'postgresql', 'libpq-dev')


   @task
   def bootstrap_collectd(c):
       """
       Bootstrap the collectd service
       """
       apt.install(c, 'collectd')
       if sync.check_isync(c, root, 'etc/collectd'):
           c.run('systemctl restart collectd')

Above you can see how WuttaMess is actually used; it simply provides
convenience functions which can be called from a Fabric task.

But `Fabric <https://www.fabfile.org>`_ (and `fabsync
<https://fabsync.ignorare.dev/>`_ for file sync operations) are doing
the heavy lifting.  The goal for WuttaMess is to further abstract
common operations and keep the task logic as "clean" as possible.

See also these functions which are used above:

* :func:`wuttamess.apt.dist_upgrade()`
* :func:`wuttamess.apt.install()`
* :func:`wuttamess.sync.make_root()`
* :func:`wuttamess.sync.check_isync()`


``files``
---------

This folder contains all files which must be synced to the target
machine as part of setup.  As shown in the example above, the
``files`` structure should "mirror" the target machine file system.

The :func:`~wuttamess.sync.check_isync()` function may be called with
a "subpath" to sync just a portion of the file system.  It returns
``True`` if any files were modified, so we can check for that and
avoid restarting services if nothing changed.

Note that in global module scope, we create the "root" object for use
with file sync.  This is then passed to the various sync functions.

This uses the ``fabsync`` library under the hood; for more on how that
works see :doc:`fabsync:index`.


``Vagrantfile``
---------------

This file is optional but may be useful for testing deployment on a
local VM using `Vagrant <https://www.vagrantup.com/>`_.  For example:

.. code-block:: ruby

   Vagrant.configure("2") do |config|

     # live machine runs Debian 12 "bookworm"
     config.vm.box = "debian/bookworm64"

   end

For more info see docs for `Vagrantfile
<https://developer.hashicorp.com/vagrant/docs/vagrantfile>`_.


.. _running-tasks:

Running Tasks via CLI
---------------------

With the above setup, first make sure you are in the right working
directory (wherever ``fabfile.py`` lives):

.. code-block:: sh

   cd myproject/machines/myserver

Then run whichever tasks you need, specifying the connection info for
target machine like so:

.. code-block:: sh

   fab -e -H root@myserver.example.com bootstrap-all

Fabric uses SSH to connect to the target machine
(myserver.example.com) and runs the specified task on that machine.

Testing with a Vagrant VM will likely require a more "complicated"
command line.  See output from ``vagrant ssh-config`` for details
specific to your VM, but the command may be something like:

.. code-block:: sh

   fab -e -H root@192.168.121.42 -i .vagrant/machines/default/libvirt/private_key bootstrap-all


Troubleshooting SSH
-------------------

In some cases troubleshooting the SSH connection can be tricky.  A rule of
thumb is to first make sure it works without Fabric.

Try a basic connection with the same args using SSH only:

.. code-block:: sh

   ssh root@myserver.example.com

Or for a Vagrant VM:

.. code-block:: sh

   ssh root@192.168.121.42 -i .vagrant/machines/default/libvirt/private_key

You may want to edit your ``~/.ssh/config`` file as needed.  However
this usually is done for "normal" machines only, not for Vagrant VM.

Once that works, then the ``fab`` command *should* also work using the
same args...
