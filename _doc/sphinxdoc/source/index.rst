.. project_name documentation documentation master file, created by
   sphinx-quickstart on Fri May 10 18:35:14 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

pymmails documentation
======================

.. image:: https://travis-ci.org/sdpython/pymmails.svg?branch=master
    :target: https://travis-ci.org/sdpython/pymmails
    :alt: Build status
   
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
   
   
**Links:** `pypi <https://pypi.python.org/pypi/pymmails/>`_,
`github <https://github.com/sdpython/pymmails/>`_,
`documentation <http://www.xavierdupre.fr/app/pymmails/helpsphinx/index.html>`_,
`wheel <http://www.xavierdupre.fr/site2013/index_code.html#pymmails>`_,
:ref:`l-README`,
:ref:`blog <ap-main-0>`

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
    
You can also send an email::

    server = create_smtp_server("gmail", "somebody", "pwd")
    send_email(server, "somebody@gmail.com", "somebody@else.com", 
                    "subject", attachements = [ os.path.abspath(__file__) ])
    server.quit()
    
    
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
    
Installation
------------

``pip install pymmails``
    

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

