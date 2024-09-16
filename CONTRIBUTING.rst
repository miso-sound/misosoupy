Contributing
============

Welcome to misosoupy contributor’s guide.

This document focuses on getting any potential contributor familiarized
with the development processes, but `other kinds of
contributions <https://opensource.guide/how-to-contribute>`__ are also
appreciated.

If you are new to using `git <https://git-scm.com>`__ or have never
collaborated in a project previously, please have a look at
`contribution-guide.org <http://www.contribution-guide.org/>`__. Other
resources are also listed in the excellent `guide created by
FreeCodeCamp <https://github.com/freecodecamp/how-to-contribute-to-open-source>`__.

Please notice, all users and contributors are expected to be **open,
considerate, reasonable, and respectful**. When in doubt, `Python
Software Foundation’s Code of
Conduct <https://www.python.org/psf/conduct/>`__ is a good reference in
terms of behavior guidelines.

Issue Reports
-------------

If you experience bugs or general issues with misosoupy, please have a
look on the `issue
tracker <https://github.com/miso-sound/misosoupy/issues>`__. If you
don’t see anything useful there, please feel free to fire an issue
report.

   Tip: Please don’t forget to include the closed issues in your search.
   Sometimes, a solution was already reported, and the problem is
   considered **solved**.

New issue reports should include information about your programming
environment (e.g., operating system, Python version) and steps to
reproduce the problem. Please try also to simplify the reproduction
steps to a very minimal example that still illustrates the problem you
are facing. By removing other factors, you help us to identify the root
cause of the issue.

Documentation Improvements
--------------------------

You can help improve misosoupy docs by making them more readable and
coherent, or by adding missing information and correcting mistakes.

misosoupy documentation uses
`Sphinx <https://www.sphinx-doc.org/en/master/>`__ as its main
documentation compiler and
`reStructuredText <https://www.sphinx-doc.org/en/master/usage/restructuredtext/>`__
markup language. This means that the docs are kept in the same
repository as the project code and that any documentation update is done
in the same way as a code contribution.

   Tip: Please notice that the `GitHub web
   interface <https://docs.github.com/en/github/managing-files-in-a-repository/managing-files-on-github/editing-files-in-your-repository>`__
   provides a quick way of propose changes in misosoupy’s files. While
   this mechanism can be tricky for normal code contributions, it works
   perfectly fine for contributing to the docs, and can be quite handy.
   If you are interested in trying this method out, please navigate to
   the docs folder in the source
   `repository <https://github.com/miso-sound/misosoupy>`__, find which
   file you would like to propose changes and click in the little pencil
   icon at the top, to open `GitHub’s code
   editor <https://docs.github.com/en/github/managing-files-in-a-repository/managing-files-on-github/editing-files-in-your-repository>`__.
   Once you finish editing the file, please write a message in the form
   at the bottom of the page describing which changes have you made and
   what are the motivations behind them and submit your proposal.

When working on documentation changes in your local machine, you can
compile them using `tox <https://tox.readthedocs.io/en/stable/>`__ :

tox -e docs

and use Python’s built-in web server for a preview in your web browser
(http://localhost:8000):

python3 -m http.server –directory ’docs/_build/html’

Code Contributions
------------------

Submit an issue
~~~~~~~~~~~~~~~

Before you work on any non-trivial code contribution it’s best to first
create a report in the `issue
tracker <https://github.com/miso-sound/misosoupy/issues>`__ to start a
discussion on the subject. This often provides additional considerations
and avoids unnecessary work.

Create an environment
~~~~~~~~~~~~~~~~~~~~~

Before you start coding, we recommend creating an isolated `virtual
environment <https://realpython.com/python-virtual-environments-a-primer/>`__
to avoid any problems with your installed Python packages. This can
easily be done via `Anaconda <https://docs.anaconda.com/index.html>`__
or `Miniconda <https://docs.conda.io/en/latest/miniconda.html>`__ and
detailed
`here <https://github.com/miso-sound/misosoupy/tree/main?tab=readme-ov-file#setup-conda-environment>`__.

Clone the repository
~~~~~~~~~~~~~~~~~~~~

1. Create an user account on GitHub if you do not already have one.

2. Fork the project
   `repository <https://github.com/miso-sound/misosoupy>`__: click on
   the *Fork* button near the top of the page. This creates a copy of
   the code under your account on GitHub.

3. Clone this copy to your local disk:

git clone git@github.com:YourLogin/misosoupy.git cd misosoupy

4. You should run:

pip install -U pip setuptools -e .

to be able to import the package under development in the Python REPL.

5. Install `pre-commit <https://pre-commit.com/>`__:

pip install pre-commit pre-commit install

misosoupy comes with a lot of hooks configured to automatically help the
developer to check the code being written.

Implement your changes
~~~~~~~~~~~~~~~~~~~~~~

1. Create a branch to hold your changes:

git checkout -b my-feature

and start making changes. Never work on the main branch!

2. Start your work on this branch. Don’t forget to add
   `docstrings <https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html>`__
   to the new functions, modules and classes, especially if they are
   part of
   `misosoupy <https://github.com/miso-sound/misosoupy/tree/main/misosoupy>`__.

3. When you’re done editing, do:

git add git commit

to record your changes in `git <https://git-scm.com>`__.

Please make sure to see the validation messages from
`pre-commit <https://pre-commit.com/>`__ and fix any eventual issues.
This should automatically use
`flake8 <https://flake8.pycqa.org/en/stable/>`__/`black <https://pypi.org/project/black/>`__
to check/fix the code style in a way that is compatible with the
project.

   **Note**: Please add unit tests and documentation in case your
   contribution adds an additional feature and is not just a bugfix.
   Moreover, writing a `descriptive commit
   message <https://chris.beams.io/posts/git-commit>`__ is highly
   recommended. In case of doubt, you can check the commit history with:
   git log –graph –decorate –pretty=oneline –abbrev-commit –all to look
   for recurring communication patterns.

Run code checks
^^^^^^^^^^^^^^^

Please make sure to see the validation messages from pre-commit and fix
any eventual issues. This should automatically use
`flake8 <https://flake8.pycqa.org/en/stable/>`__/`black <https://pypi.org/project/black/>`__
to check/fix the code style in a way that is compatible with the
project.

To run pre-commit manually, you can use:

pre-commit run –all-files

Please also check that your changes don’t break any unit tests with:

tox

(after having installed `tox <https://tox.readthedocs.io/en/stable/>`__
with pip install tox or pipx).

You can also use `tox <https://tox.readthedocs.io/en/stable/>`__ to run
several other pre-configured tasks in the repository. Try tox -av to see
a list of the available checks.

Submit your contribution
~~~~~~~~~~~~~~~~~~~~~~~~

1. If everything works fine, push your local branch to the remote server
   with:

git push -u origin my-feature

2. Go to the web page of your fork and click “Create pull request” to
   send your changes for review.

   Find more detailed information in `creating a
   PR <https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request>`__.
   You might also want to open the PR as a draft first and mark it as
   ready for review after the feedbacks from the continuous integration
   (CI) system or any required fixes.

Troubleshooting
~~~~~~~~~~~~~~~

The following tips can be used when facing problems to build or test the
package:

1. Make sure to fetch all the tags from the upstream
   `repository <https://github.com/miso-sound/misosoupy>`__. The command
   git describe –abbrev=0 –tags should return the version you are
   expecting. If you are trying to run CI scripts in a fork repository,
   make sure to push all the tags. You can also try to remove all the
   egg files or the complete egg folder, i.e., .eggs, as well as the
   \*.egg-info folders in the src folder or potentially in the root of
   your project.

2. Sometimes `tox <https://tox.readthedocs.io/en/stable/>`__ misses out
   when new dependencies are added, especially to setup.cfg and
   docs/requirements.txt. If you find any problems with missing
   dependencies when running a command with
   `tox <https://tox.readthedocs.io/en/stable/>`__, try to recreate the
   tox environment using the -r flag. For example, instead of:

tox -e docs

Try running:

tox -r -e docs

3. Make sure to have a reliable
   `tox <https://tox.readthedocs.io/en/stable/>`__ installation that
   uses the correct Python version (e.g., 3.7+). When in doubt you can
   run:

tox –version # OR which tox

If you have trouble and are seeing weird errors upon running
`tox <https://tox.readthedocs.io/en/stable/>`__, you can also try to
create a dedicated `virtual
environment <https://realpython.com/python-virtual-environments-a-primer/>`__
with a `tox <https://tox.readthedocs.io/en/stable/>`__ binary freshly
installed. For example:

virtualenv .venv source .venv/bin/activate .venv/bin/pip install tox
.venv/bin/tox -e all

4. `Pytest can drop
   you <https://docs.pytest.org/en/stable/usage.html#dropping-to-pdb-python-debugger-at-the-start-of-a-test>`__
   in an interactive session in the case an error occurs. In order to do
   that you need to pass a –pdb option (for example by running tox – -k
   –pdb). You can also setup breakpoints manually instead of using the
   –pdb option.

Maintainer tasks
----------------

Releases
~~~~~~~~

If you are part of the group of maintainers and have correct user
permissions on `PyPI <https://pypi.org/>`__, the following steps can be
used to release a new version for misosoupy:

1. Make sure all unit tests are successful.
2. Tag the current commit on the main branch with a release tag, e.g.,
   v1.2.3.
3. Push the new tag to the upstream
   `repository <https://github.com/miso-sound/misosoupy>`__, e.g., git
   push upstream v1.2.3
4. Clean up the dist and build folders with tox -e clean (or rm -rf dist
   build) to avoid confusion with old builds and Sphinx docs.
5. Run tox -e build and check that the files in dist have the correct
   version (no .dirty or `git <https://git-scm.com>`__ hash) according
   to the `git <https://git-scm.com>`__ tag. Also check the sizes of the
   distributions, if they are too big (e.g., > 500KB), unwanted clutter
   may have been accidentally included.
6. Run tox -e publish – –repository pypi and check that everything was
   uploaded to `PyPI <https://pypi.org/>`__ correctly.
