Pbundle
=======

Simple python dependency manager with a lock file, much like composer for php or
bundler for ruby.

Principles and Motivation
-------------------------

* repeatable dependencies for all deployments (including development systems)

* the dependency manager is not a build system

* the system python is worth compromising for but we don't require it

* standard tools are worth compromising for

* the dependency manager is not necessarily a deployment tool; deb, rpm etc is
  probably better so we should support them

* software should not depend on its dependency manager

* os distributors are not the enemy and actually do a lot of useful work

Usage: Initial Install
----------------------

If you do not have a global install of pbundle (or want to use the version from
git) then there is a zero-config install::

  $ python pbootstrap.py

In your repository will be created a simple virtual environment with pbundle
installed, by default in ``pbundle_modules``.

Write a requirements.txt to define your dependencies and run an update::

  $ pbundle update

This will create and update a virtual environment (in ``python_modules`` by
default) with your specified dependencies and write a lock file, which is simply
another ``requirements.txt`` with exact versions in it.  You should commit the
lock file to your VCS.

If you used the bootstrap script you can add pbundle to your requirements.txt so
that you don't need two virtualenvs, but pbundle does not need to be in the same
environment as your project.

Usage: Deployment
-----------------

Once your lock file is committed to vcs, use::

  $ pbundle install

To apply the changes to your virtual environment.

Usage: Update Dependencies
--------------------------

Update from your requirements.txt again::

  $ pbundle update

Commit the lock file so that other deployments can apply your changes.

Usage: Maintenance
------------------

Verify your virtual environment is up to date with the lock file::

  $ pbundle verify

It's a good idea to integrate this into your deployment and CI system.

Typically python packages are quite good at keeping compatibility so it can be a
good idea to have at least one build running against the most recent
dependencies rather than the lock file.
