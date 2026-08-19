.. _launchpad-namespaces:

Launchpad repository paths (namespaces)
=======================================

A Launchpad repository path tells users *who owns* the repository and *what
it's for*. Every repository has a unique path built from these parts:

- an **owner**, always written with a leading tilde, such as ``~jane`` for a
  person or ``~my-team`` for a team;
- an optional **target** that the repository belongs to, such as a project
  (``launchpad``) or a distribution source package
  (``ubuntu/+source/hello``);
- the literal marker ``+git`` followed by the **repository name**.

Common repository paths
-----------------------

Common path shapes include:

- ``~OWNER/PROJECT/+git/REPOSITORY`` — a repository for a project, for example
  ``~jane/launchpad/+git/launchpad``.
- ``~OWNER/+git/REPOSITORY`` — a "personal" repository not attached to any
  project, for example ``~jane/+git/experiments``.
- ``~OWNER/DISTRIBUTION/+source/SOURCE/+git/REPOSITORY`` — a forked repository
  for a source package in a distribution.

The part of the path up to and including the owner and target (project or
package) is the **namespace**. Pushing into a namespace you're allowed to write
to is how you create repositories: if you push to ``~jane/launchpad``,
Launchpad creates that repository under Jane; if you push to ``~my-team/launchpad``,
it creates one owned by the team so every member can push to it.

Default paths
-------------

Launchpad also recognises shorter **default** paths that skip the owner, such
as: 

- ``https://code.launchpad.net/PROJECT`` for a project's default repository
- ``https://code.launchpad.net/DISTRIBUTION/+source/SOURCE`` for the default
  repository for a source package in a distribution.
- ``https://code.launchpad.net/~OWNER/PROJECT`` for an an owner’s default
  repository for an upstream project.
- ``https://code.launchpad.net/~OWNER/DISTRIBUTION/+source/SOURCE`` for an
  owner’s default repository for a source package in a distribution. 

Projects hosting their code on Launchpad usually have their primary repository
set as the default for the project. Contributors usually push to branches in
owner-default repositories. The extra flexibility with named repositories
allows for situations such as separate private repositories containing
embargoed security fixes.

For examples on how namespaces work for team repositories,
see :ref:`team repositories <team-repositories>`.