.. meta::
   :description: Building Debian (.deb) packages in Launchpad by uploading a
      signed source package to a PPA.

.. _build-deb-packages-in-launchpad:

Build Debian packages in Launchpad
==================================

The easiest way to build a Debian (``.deb``) package is to let Launchpad do it
for you. You build a *source* package on your own machine, sign it, and upload
it to a :ref:`Personal Package Archive (PPA) <personal-package-archive>`.
Launchpad then compiles the binary packages for each declared architecture
using the same builders as the official Ubuntu archive, and publishes them so
anyone can install them.

Building this way means you don't have to run your own build infrastructure,
and the resulting packages are publicly available which is handy for sharing
test builds with bug reporters or reviewers.

.. note::

   Launchpad builds packages from *source* and does not accept pre-built
   ``.deb`` files. You only upload a source package (a ``.dsc`` and its related
   files).

Prerequisites
-------------

Before you start, make sure you have:

- An **OpenPGP key registered on your account**. Launchpad only accepts uploads
  signed by a key it knows. Add your key at ``https://launchpad.net/~/+editpgpkeys``.

- A **PPA to upload to**. If you don't have one yet, see :ref:`create-ppa`.

- The **packaging tools installed**. You will need these to edit the changelog,
  build the source package, sign the upload with your GPG key, and upload it::

    sudo apt install devscripts dpkg-dev dput


Set your packaging identity
---------------------------

Package tools stamp each changelog entry with an author name and email. Set
these to match the identity of the key registered on your Launchpad account, so
the changelog and the signature agree::

    export DEBFULLNAME="Your Name"
    export DEBEMAIL="you@example.com"

Get the package source
----------------------

Fetch the source of the package you want to build. For an existing Ubuntu
package::

    apt-get source <package>
    cd <package>-*/

If you are `packaging your own software <https://ubuntu.com/project/docs/contributors/new-package/create-a-new-package/>`_,
start from your existing source tree containing a
`debian/ directory <https://ubuntu.com/project/docs/how-ubuntu-is-made/concepts/debian-directory/>`_.

Set a PPA-specific version
--------------------------

A PPA won't accept a version string that clashes with one already in the
archive, and it won't accept the same version twice. You must add a suffix to
the version in ``debian/changelog`` so it is unique to your PPA.

The tilde (``~``) character sorts *lower* than everything else, so appending
``~<label>1`` keeps your PPA version just *below* the official one -- which is
what you want for a rebuild. Use ``dch`` to add the entry, naming the Ubuntu
release you are targeting as both the suffix and the distribution::

    codename="noble"
    dch -l "~${codename}" --distribution "${codename}" "Build for PPA"

For example, this turns ``hello (2.10-5build1)`` into
``hello (2.10-5build1~noble1)``. Set ``codename`` to the release you are
building for (for example ``noble`` for 24.04, ``jammy`` for 22.04).

.. important::

   Include a **number** at the end of the suffix (``~noble1``, ``~noble2``,
   ...). Once Launchpad accepts an upload, it will not accept another upload
   with the same or a lower version. If you need to fix anything and re-upload,
   increment the number.

Using the release codename in the suffix is optional, but it makes each version
unique per release and shows users which package matches which Ubuntu release.
This is useful if you later build the same fix for several releases. See the
Ubuntu project docs for
`more details on versioning <https://ubuntu.com/project/docs/how-ubuntu-is-made/concepts/version-strings/>`_.

Build the signed source package
--------------------------------

After setting the version, you need to build a source-only package.
``dpkg-buildpackage`` reads the version from the top of ``debian/changelog``
and produces the ``.dsc``, ``.debian.tar.*`` and ``.changes`` files in the
parent directory::

    dpkg-buildpackage -S -I -i -nc -d

- ``-S`` builds a source package.
- ``-I`` and ``-i`` exclude version-control and backup files.
- ``-nc`` skips cleaning so the tree is left as-is.
- ``-d`` skips the build-dependency check, which isn't needed for a source
  build.

If a signing key is available, this step also signs the files.

You may see a warning that the new version is "earlier than the previous one".
This is expected for a PPA rebuild because of versioning rules that ensure if
the package in the official archive is updated, it will be chosen over yours.
See this section on `comparing versions <https://ubuntu.com/project/docs/how-ubuntu-is-made/concepts/version-strings/#comparing-versions>`_
for more details.

Sign the source package
-----------------------

The upload must be signed by the key registered on your Launchpad account. If
``dpkg-buildpackage`` did not sign the files (for example, because no key was
available at build time), sign them explicitly with ``debsign``, naming the key
to be sure the right one is used::

    debsign -k <your-key-id> ../<package>_<version>_source.changes

Find your key ID with::

    gpg --list-secret-keys --keyid-format long

``debsign`` signs both the ``.dsc`` and ``.changes`` files. You will be prompted
for your key passphrase.

Upload to your PPA
------------------

Upload the ``.changes`` file with ``dput``. Launchpad reads it and pulls in the
referenced ``.dsc`` and source tarball::

    dput ppa:<username>/<ppa-name> ../<package>_<version>_source.changes

For the ``hello`` example targeting the ``personal`` PPA::

    dput ppa:<username>/personal ../hello_2.10-5build1~noble1_source.changes

For more upload options (SFTP, custom ``dput`` targets, team PPAs), see
:ref:`upload-a-package-to-a-ppa`.

Watch the build
---------------

You must wait for Launchpad to build the package server-side before you can
install from the PPA. This can take anywhere from a few minutes to a few hours,
depending on how busy the build farm is.

Launchpad will send you an **Accepted** or **Rejected** notice via email once
it checks the signature and version, then sends build-status mails per
architecture. You can also watch progress on the PPA's package page::

    https://launchpad.net/~<your-lp-id>/+archive/ubuntu/<ppa-name>/+packages

Launchpad first builds the binaries for each enabled architecture, then
publishes the source and binary packages for public download.

.. note::

   A PPA keeps only **one** version of a given source package per Ubuntu series
   -- the highest one. Uploading a newer version *supersedes* the previous one
   (the old version stays visible in the publishing history). Uploading the same
   or a lower version is rejected.

Next steps
----------

- :ref:`Install packages from a PPA <install-software-from-ppas>`.
- If the upload was rejected, see
  :ref:`what the upload errors mean <troubleshoot-package-upload-errors>`.
- :ref:`Delete packages from a PPA <package-deletion>`.
