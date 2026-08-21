.. meta::
   :description: Complete guide to everyday git operations on Launchpad,
      including cloning, pushing, pulling, forking, and syncing with upstream.

.. _perform-git-operations:

Perform git operations in Launchpad
===================================

When working with code hosted on Launchpad, you'll need to perform git
operations such as forking and cloning repositories, pushing and pulling
changes to and from upstream branches, merging changes into other branches, etc.

Many of these operations are identical to how you may have worked with other
codehosting platforms that support git. However, there are some nuances to how
some operations are performed in Launchpad.

Prerequisites
-------------

To follow this guide, you need:

- A Launchpad account. See
  :ref:`how to create an account <create-and-personalise-your-launchpad-account>`.
- A way to authenticate with Launchpad:

  - **SSH** (recommended for pushing your own code): `add your public key <https://launchpad.net/~/+editsshkeys>`_
    to your Launchpad account. See :ref:`import your SSH keys <import-your-ssh-keys>`.
  - **HTTPS**: use an access token as your password. See the "HTTPS
    authentication" section of :ref:`hosting Git repositories <hosting-git-repositories>`.

- Basic `knowledge of Git <https://gitimmersion.com/>`_ and Git installed on
  your machine.

Clone a repository
------------------

You need a repository's path in Launchpad to clone it. Launchpad repositories
have unique paths. To find out more about these, see :ref:`Launchpad namespaces <launchpad-namespaces>`.
You can also modify your `.gitconfig` file to :ref:`shorten these paths <hosting-git-repositories>`.

To clone a project's default repository:

::

   git clone git+ssh://<username>@git.launchpad.net/PROJECT

For example, ``git clone git+ssh://<username>@git.launchpad.net/lpci``
clones the Launchpad lpci repository.

You can also clone a specific repository by its full path:

::

   git clone git+ssh://<username>@git.launchpad.net/~OWNER/PROJECT/+git/REPOSITORY

You can also clone read-only repositories over HTTPS without SSH keys:

::

   git clone https://git.launchpad.net/PROJECT

You will be prompted to confirm the SSH fingerprint when you connect over SSH
for the first time. Verify the :ref:`host fingerprint <ssh-fingerprints>`
before accepting the connection.

Push a branch
-------------

If you own the repository (or are a member of the owning team), you can push
branches directly.

Add the repository as a remote, then push your branch:

::

   git remote add origin git+ssh://<username>@git.launchpad.net/~OWNER/PROJECT/+git/REPOSITORY
   git push -u origin my-branch

If the repository doesn't exist yet, pushing into a namespace you can write to
creates it automatically. For example, to create a personal repository:

::

   git remote add origin git+ssh://<username>@git.launchpad.net/~<username>/+git/REPOSITORY
   git push -u origin main

After a push, Launchpad scans the repository and prints guidelines (visible in
the :guilabel:`Code` tab) that you can use to merge changes from the branch you
just pushed to the main branch.

Pull and keep your clone up to date
-----------------------------------

To bring the latest commits from Launchpad into your current branch:

::

   git pull <remote> <branch>

This is shorthand for fetching new commits from the remote and merging them
into your checked-out branch. If your local branch is already set to track an
upstream branch, you can simply do a ``git pull`` without specifying ``remote``
and ``branch``. 

If you'd rather review what changed before integrating it, fetch first and then
merge or rebase:

::

   git fetch origin
   git merge origin/main        # or: git rebase origin/main

Fork a repository
-----------------

If you want to contribute to a repository that you don't own, it's a good idea
to first create your own fork that you can push to freely. The fork will be
under your account's namespace.

To fork a repository through the web UI:

#. Go to the repository's code page, i.e.,
   ``https://code.launchpad.net/PROJECT``.
#. Select :guilabel:`Fork it to your account`.

Launchpad creates your fork at a path under your account, such as
``~<username>/PROJECT/+git/PROJECT``. On your fork's page, under
:guilabel:`Get this repository`, you'll find the exact clone command.

When you push a new branch with changes to your fork, a new link is created
that you can follow to open a merge proposal on the upstream repository:

::

   https://code.launchpad.net/~<username>/PROJECT/+git/PROJECT/+ref/<branch>/+register-merge

See :ref:`create and manage a merge proposal <create-and-manage-a-merge-proposal>`
for the full review workflow.

Sync your fork with upstream
----------------------------

Over time, the upstream repository that you forked from may gain new commits.
To pull those into your fork, add the upstream repository as a second remote.

#. On the original repository's code page, under :guilabel:`Get this
   repository`, copy the repository URL, for example
   ``git+ssh://<username>@git.launchpad.net/PROJECT``.

#. In your local clone, add it as a remote named ``upstream``:

   ::

      git remote add upstream git+ssh://<username>@git.launchpad.net/PROJECT

#. Fetch and integrate upstream changes into your branch, e.g., ``main``:

   ::

      git pull upstream main

#. Push the refreshed history to your fork (``origin``) so it stays in sync:

   ::

      git push origin main

You now have two remotes: ``origin`` (your fork, which you push to) and
``upstream`` (the original repository, which you pull from). This is the
standard setup for contributing changes over time.

Next steps
----------

- Turn a pushed branch into a review request:
  :ref:`create and manage a merge proposal <create-and-manage-a-merge-proposal>`.
- Host a project's code for the first time:
  :ref:`host your project's code on Launchpad <host-your-project-code-on-launchpad>`.
- Share a repository with several people:
  :ref:`team repositories <team-repositories>`.
- Understand the hosting model in depth:
  :ref:`hosting Git repositories <hosting-git-repositories>`.
