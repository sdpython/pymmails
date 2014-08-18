.. _l-README:

README
======

   
**Links:**
    * `pypi/pymmails <https://pypi.python.org/pypi/pymmails/>`_
    * `GitHub/pymmails <https://github.com/sdpython/pymmails/>`_
    * `documentation <http://www.xavierdupre.fr/app/pymmails/helpsphinx/index.html>`_
    * `Windows Setup <http://www.xavierdupre.fr/site2013/index_code.html#pymmails>`_


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

* **v0.3 - 2014/??/??**
    * **change:** add a version parameter

