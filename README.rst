SSH Vampire
===========

This script scans all processes belonging to a user (defaulting to the
current user) for ssh-agent environment variables, and prints those
environment variables to stdout.

This might be useful if you ssh into a desktop or workstation that is
running ssh-agent, and then wish to connect to another computer, using
the keys stored in ssh-agent. In that case, you'll want to run::

    workstation$ eval $(ssh_vampire.py)
    workstation$ ssh other_computer


Requirements
------------

SSH Vampire is linux-specific. It requires the /proc filesystem to do
its work.

SSH Vampire requires Python 3 to be installed.


Installation
------------

``ssh_vampire.py`` can be run directly from the checkout, or can be copied
some place in your path.

