============
Contributing
============

.. contents::

Issue Reporting
===============

**Before Creating an Issue:**

- Check `GitHub Issues`_ to see if the issue already exists
- If the issue hasn't been reported yet and appears to be related to selenium,
  check `Selenium's GitHub Issues`_ to see if the issue exists
- If the issue isn't reported there and appears to be specific to WebDriver Test
  Tools, `open a new issue`_ and fill out the required details, being as
  specific as possible

.. _Github Issues: https://github.com/connordelacruz/webdriver-test-tools/issues
.. _open a new issue: https://github.com/connordelacruz/webdriver-test-tools/issues/new
.. _Selenium's GitHub Issues: https://github.com/SeleniumHQ/selenium/issues


Pull Requests
=============

**Note:**

    The project is currently the in early stages of development, and as such the
    workflow for pull requests hasn't been formalized. These guidelines are a
    work in progress and will be expanded upon as the project develops.

TODO
----

- Formalize feature branch workflow


Branch Structure
----------------

There are 2 main branches for this project:

- **master:** The main branch where source code is ready for production
- **develop:** The working branch for the next release

New features for upcoming releasese should have their own feature branch. When
development on the feature is finished, a pull request should be submitted to
merge into the **develop** branch.

Once the develop branch is at a stable point and is ready for release, it will
be merged into master and tagged with a release number.

