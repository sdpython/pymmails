
.. image:: https://github.com/sdpython/pymmails/blob/master/_doc/sphinxdoc/source/phdoc_static/project_ico.png?raw=true
    :target: https://github.com/sdpython/pymmails/

.. _l-README:

pymmails: send and grab mails
=============================

.. only:: html

    .. image:: https://travis-ci.com/sdpython/pymmails.svg?branch=master
        :target: https://app.travis-ci.com/github/sdpython/pymmails
        :alt: Build status

    .. image:: https://ci.appveyor.com/api/projects/status/hqhhdndvayrx0r9k?svg=true
        :target: https://ci.appveyor.com/project/sdpython/pymmails
        :alt: Build Status Windows

    .. image:: https://circleci.com/gh/sdpython/pymmails/tree/master.svg?style=svg
        :target: https://circleci.com/gh/sdpython/pymmails/tree/master

    .. image:: https://badge.fury.io/py/pymmails.svg
        :target: http://badge.fury.io/py/pymmails

    .. image:: http://img.shields.io/github/issues/sdpython/pymmails.png
        :alt: GitHub Issues
        :target: https://github.com/sdpython/pymmails/issues

    .. image:: https://img.shields.io/badge/license-MIT-blue.svg
        :alt: MIT License
        :target: http://opensource.org/licenses/MIT

    .. image:: https://codecov.io/github/sdpython/pymmails/coverage.svg?branch=master
        :target: https://codecov.io/github/sdpython/pymmails?branch=master

The module was started to grab emails using IMAP and to store them on a local disk.
It is now used to download material sent by students before an oral presentation,
which is quite annoying to do manually.

::

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

**Links:**

* `GitHub/pymmails <https://github.com/sdpython/pymmails/>`_
* `documentation <http://www.xavierdupre.fr/app/pymmails/helpsphinx/index.html>`_
* `Blog <http://www.xavierdupre.fr/app/pymmails/helpsphinx/blog/main_0000.html#ap-main-0>`_
