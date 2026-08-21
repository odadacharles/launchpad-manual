.. _launchpad-namespaces:

Launchpad repository paths (namespaces)
=======================================

A Launchpad repository path tells users *who owns* the repository and *what
it is for*. Every repository has a unique path built from these parts:

- an **owner**, always written with a leading tilde, such as ``~jane`` for a
  person or ``~my-team`` for a team;
- an optional **target** that the repository belongs to, such as a project
  (``lpci``) or a distribution source package
  (``ubuntu/+source/hello``);
- the literal marker ``+git`` 
- the **repository name**.

Common repository paths
-----------------------

Common path shapes include:

- ``~OWNER/PROJECT/+git/REPOSITORY`` — a repository for a project, for example
  ``~jane/lpci/+git/lpci``.
- ``~OWNER/+git/REPOSITORY`` — a "personal" repository not attached to any
  project, for example ``~jane/+git/experiments``.
- ``~OWNER/DISTRIBUTION/+source/SOURCE/+git/REPOSITORY`` — a forked repository
  for a source package in a distribution, for example
  ``~jane/ubuntu/+source/hello/+git/hello``.

The part of the path up to and including the owner and target (project or
package) is the **namespace**. Pushing into a namespace where you have write
permissions is how you create repositories. If you push to ``~jane/lpci``,
Launchpad creates that repository under Jane's ownership; if you push to
``~my-team/lpci``, it creates one owned by that team so every member of
the team can push to it.

Default paths
-------------

Launchpad also recognises shorter **default** paths that skip the owner. 
Projects hosting their code on Launchpad usually have a repository set as the
default for the project. Contributors fork these default repositories and push
to a branch of the fork. The extra flexibility with named repositories allows
for situations such as separate private repositories containing embargoed
security fixes.

Common default path shapes include:

- ``https://code.launchpad.net/PROJECT`` for a project's default repository
- ``https://code.launchpad.net/DISTRIBUTION/+source/SOURCE`` for the default
  repository of a source package in a distribution.
- ``https://code.launchpad.net/~OWNER/PROJECT`` for an owner’s (person or team)
  default repository for a forked upstream project.
- ``https://code.launchpad.net/~OWNER/DISTRIBUTION/+source/SOURCE`` for an
  owner’s (person or team) default repository for a forked source package in a
  distribution. 

For examples on how namespaces work for team repositories,
see :ref:`team repositories <team-repositories>`.