
pymmails documentation
======================

.. only:: html

    .. image:: https://travis-ci.org/sdpython/pymmails.svg?branch=master
        :target: https://travis-ci.org/sdpython/pymmails
        :alt: Build status

    .. image:: https://ci.appveyor.com/api/projects/status/hqhhdndvayrx0r9k?svg=true
        :target: https://ci.appveyor.com/project/sdpython/pymmails
        :alt: Build Status Windows

    .. image:: https://badge.fury.io/py/pymmails.svg
        :target: http://badge.fury.io/py/pymmails

    .. image:: http://img.shields.io/github/issues/sdpython/pymmails.png
        :alt: GitHub Issues
        :target: https://github.com/sdpython/pymmails/issues

    .. image:: https://img.shields.io/badge/license-MIT-blue.svg
        :alt: MIT License
        :target: http://opensource.org/licenses/MIT

    .. image:: https://landscape.io/github/sdpython/pymmails/master/landscape.svg?style=flat
       :target: https://landscape.io/github/sdpython/pymmails/master
       :alt: Code Health

    .. image:: https://requires.io/github/sdpython/pymmails/requirements.svg?branch=master
         :target: https://requires.io/github/sdpython/pymmails/requirements/?branch=master
         :alt: Requirements Status

    .. image:: https://codecov.io/github/sdpython/pymmails/coverage.svg?branch=master
        :target: https://codecov.io/github/sdpython/pymmails?branch=master

**Links:** `pypi <https://pypi.python.org/pypi/pymmails/>`_,
`github <https://github.com/sdpython/pymmails/>`_,
`documentation <http://www.xavierdupre.fr/app/pymmails/helpsphinx/index.html>`_,
`wheel <http://www.xavierdupre.fr/site2013/index_code.html#pymmails>`_,
:ref:`l-README`,
:ref:`blog <ap-main-0>`,
:ref:`l-issues-todolist`

What is it?
-----------

The module was started to grab emails using IMAP and to store them on a local disk.
I now use it to download to material sent by my students before an oral presentation.
I receive many of them and it is usually annoying to download them one by one.
Here is the code I use::

    from pymmails import MailBoxImap, EmailMessageRenderer

    user = "your.email"
    pwd = "passsword"
    server = "imap.your_provider.ext"

    box = MailBoxImap(user, pwd, server)
    render = EmailMessageRenderer()
    box.login()
    for mail in box.enumerate_mails_in_folder("saved", pattern="<pattern>") :
        mail.dump(render, location=temp, fLOG=fLOG)
    box.logout()
    render.flush()

Some examples of patterns::

    pattern='FROM "xavier" SINCE 1-Feb-2013'
    pattern='FROM "xavier" SINCE 1-Feb-2013 BEFORE 5-May-2013'
    pattern='FROM "xavier" SINCE 1-Feb-2013 BEFORE 5-May-2013 UNANSWERED'
    pattern='CC "jacques" FROM "xavier" DELETED'
    pattern='TEXT "github"'
    pattern='LARGER 10000 SMALLER 1000000'
    pattern='SUBJECT "programmation"'
    pattern='TO "student" FLAGGED'
    pattern='UNSEEN'

See `pattern specifications <https://tools.ietf.org/html/rfc3501#page-49>`_.

Installation
------------

``pip install pymmails``

Galleries
---------

.. toctree::
    :maxdepth: 2

    api/index
    gyexamples/index
    gynotebooks/index

Functionalities
---------------

* download email and attchments from an server IMAP4 (gmail for example)
* search for recent emails

By default, IMAP functionalities are not enabled on gmail (if you have
a gmail account), it can be enabled from the settings page
(see `Enable POP and IMAP for Google Apps <https://support.google.com/a/answer/105694>`_).

Indices and tables
------------------

+----------------------+---------------------+---------------------+--------------------+------------------------+------------------------------------------------+
| :ref:`l-modules`     |  :ref:`l-functions` | :ref:`l-classes`    | :ref:`l-methods`   | :ref:`l-staticmethods` | :ref:`l-properties`                            |
+----------------------+---------------------+---------------------+--------------------+------------------------+------------------------------------------------+
| :ref:`modindex`      |  :ref:`l-example`   | :ref:`search`       | :ref:`l-license`   | :ref:`l-changes`       | :ref:`l-README`                                |
+----------------------+---------------------+---------------------+--------------------+------------------------+------------------------------------------------+
| :ref:`genindex`      |  :ref:`l-FAQ`       | :ref:`l-notebooks`  |                    | :ref:`l-statcode`      | `Unit Test Coverage <coverage/index.html>`_    |
+----------------------+---------------------+---------------------+--------------------+------------------------+------------------------------------------------+

Navigation
----------

.. toctree::
    :maxdepth: 1

    indexmenu
