

.. _l-README:

README / Changes
================

.. image:: https://travis-ci.org/sdpython/pymmails.svg?branch=master
    :target: https://travis-ci.org/sdpython/pymmails
    :alt: Build status

.. image:: https://ci.appveyor.com/api/projects/status/isbawgkh38kmw0lw?svg=true
    :target: https://ci.appveyor.com/project/sdpython/pymmails
    :alt: Build Status Windows
    
.. image:: https://badge.fury.io/py/pymmails.svg
    :target: http://badge.fury.io/py/pymmails
   
.. image:: http://img.shields.io/pypi/dm/pymmails.png
    :alt: PYPI Package
    :target: https://pypi.python.org/pypi/pymmails

.. image:: http://img.shields.io/github/issues/sdpython/pymmails.png
    :alt: GitHub Issues
    :target: https://github.com/sdpython/pymmails/issues
    
.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :alt: MIT License
    :target: http://opensource.org/licenses/MIT      

**Links:**
    * `pypi/pymmails <https://pypi.python.org/pypi/pymmails/>`_
    * `GitHub/pymmails <https://github.com/sdpython/pymmails/>`_
    * `documentation <http://www.xavierdupre.fr/app/pymmails/helpsphinx/index.html>`_
    * `Windows Setup <http://www.xavierdupre.fr/site2013/index_code.html#pymmails>`_
    * `Travis <https://travis-ci.org/sdpython/pymmails>`_
    * `Blog <http://www.xavierdupre.fr/app/pymmails/helpsphinx/blog/main_0000.html#ap-main-0>`_


Description
-----------

The module was started to grab emails using IMAP and to store them on a local disk.
I now use it to download to material sent by my students before an oral presentation.
I receive many of them and it is usually annoying to download them one by one.
Here is the code I use::

    from pyquickhelper import fLOG
    from pymmails import MailBoxImap
    fLOG(OutputPrint=True)
    user = "your.email"
    pwd = "passsword"
    server = "imap.your_provider.ext"
    box = MailBoxImap(user, pwd, server)
    box.login()
    box.dump_html(folder=os.path.abspath(r"folder_destination"))
    box.logout()
    
A parameter ``pattern`` can be added to look for a subset of emails::    

    ...
    box.dump_html(folder=os.path.abspath(r"folder_destination"),
                pattern='FROM "xavier"')
    ...
    
Below, some examples of patterns::

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
    

Versions
--------

* **0.3 - 2014/??/??**
    * **change:** add a version parameter
    * **fix:** the setup does not need the file ``README.rst`` anymore
    * **add:** method *pymmails.grabber.email_message.EmailMessage.get_to*
    * **add:** method *pymmails.grabber.mailboximap.MailBoxImap.enumerate_search_person* to grap all emails received from or send to a person
    * **fix:** fix paths of embedded images in emails when dumping them on disk
    * **new:** functions to send emails, see *pymmails.sender.email_sender*

