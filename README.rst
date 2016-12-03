

.. _l-README:

README
======

.. image:: https://travis-ci.org/sdpython/pymmails.svg?branch=master
    :target: https://travis-ci.org/sdpython/pymmails
    :alt: Build status

.. image:: https://ci.appveyor.com/api/projects/status/isbawgkh38kmw0lw?svg=true
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
   


**Links:**

* `GitHub/pymmails <https://github.com/sdpython/pymmails/>`_
* `documentation <http://www.xavierdupre.fr/app/pymmails/helpsphinx/index.html>`_
* `Blog <http://www.xavierdupre.fr/app/pymmails/helpsphinx/blog/main_0000.html#ap-main-0>`_


Description
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
    
Design
------

This project contains various helper about logging functions, unit tests and help generation.

* a source folder: ``src``
* a unit test folder: ``_unittests``, go to this folder and run ``run_unittests.py``
* a _doc folder: ``_doc``, it will contains the documentation
* a file ``setup.py`` to build and to install the module
* a file ``make_help.py`` to build the sphinx documentation
    
