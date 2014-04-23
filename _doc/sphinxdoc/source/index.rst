.. project_name documentation documentation master file, created by
   sphinx-quickstart on Fri May 10 18:35:14 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

pymmails documentation
======================

   
   
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
    

Functionalities
---------------

* download email and attchments from an server IMAP4 (gmail for example)
* search for recent emails


About this documentation
------------------------

.. toctree::
    :maxdepth: 1

    doctestunit
    generatedoc
    generatesetup
    installation
    all_example
    all_FAQ
    all_notebooks
    glossary
    index_module

    
Indices and tables
==================

+------------------+---------------------+------------------+------------------+------------------------+---------------------+
| :ref:`l-modules` |  :ref:`l-functions` | :ref:`l-classes` | :ref:`l-methods` | :ref:`l-staticmethods` | :ref:`l-properties` |
+------------------+---------------------+------------------+------------------+------------------------+---------------------+
| :ref:`genindex`  |  :ref:`modindex`    | :ref:`search`    | :ref:`l-license` | :ref:`l-changes`       | :ref:`l-README`     |
+------------------+---------------------+------------------+------------------+------------------------+---------------------+
| :ref:`l-example` |  :ref:`l-FAQ`       |                  |                  |                        |                     |
+------------------+---------------------+------------------+------------------+------------------------+---------------------+
   

   

