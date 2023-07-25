
===================================
Python connector for SQream DB Blue
===================================

* **Version:**  1.0.31

* **Supported SQream DB versions:** >= Blue cloud

The Python connector for SQream DB is a Python DB API 2.0-compliant interface for developing Python applications with SQream DB.

The SQream Python connector provides an interface for creating and running Python applications that can connect to a SQream DB database. It provides a lighter-weight alternative to working through native C++ or Java bindings, including JDBC and ODBC drivers.

pysqream conforms to Python DB-API specifications `PEP-249 <https://www.python.org/dev/peps/pep-0249/>`_

``pysqream_blue`` is native and pure Python, with minimal requirements. It can be installed with ``pip3`` on any operating system, including Linux, Windows, and macOS.

.. For more information and a full API reference, see `SQream documentation's pysqream blue guide <https://sqream-docs.readthedocs.io/en/latest/guides/client_drivers/python/index.html>`_ .

Requirements
-------------

* Python 3.9+

Installing the Python connector
--------------------------------

Prerequisites
----------------

1. Python
^^^^^^^^^^^^

The connector requires Python 3.9 or newer. To verify your version of Python:

.. code-block:: console

   $ python --version
   Python 3.9

2. PIP
^^^^^^^^^^^^
The Python connector is installed via ``pip3``, the Python package manager and installer.

We recommend upgrading to the latest version of ``pip3`` before installing. To verify that you are on the latest version, run the following command:

.. code-block:: console

   $ python -m pip3 install --upgrade pip
   Collecting pip
      Downloading https://files.pythonhosted.org/packages/00/b6/9cfa56b4081ad13874b0c6f96af8ce16cfbc1cb06bedf8e9164ce5551ec1/pip-19.3.1-py2.py3-none-any.whl (1.4MB)
        |████████████████████████████████| 1.4MB 1.6MB/s
   Installing collected packages: pip
     Found existing installation: pip 19.1.1
       Uninstalling pip-19.1.1:
         Successfully uninstalled pip-19.1.1
   Successfully installed pip-19.3.1

.. note::
   * On macOS, you may want to use virtualenv to install Python and the connector, to ensure compatibility with the built-in Python environment
   *  If you encounter an error including ``SSLError`` or ``WARNING: pip is configured with locations that require TLS/SSL, however the ssl module in Python is not available.`` - please be sure to reinstall Python with SSL enabled, or use virtualenv or Anaconda.


Install via pip
-----------------

The Python connector is available via `PyPi <https://pypi.org/project/pysqream/>`_.

Install the connector with ``pip3``:

.. code-block:: console

   $ pip3 install pysqream-blue

``pip3`` will automatically installs all necessary libraries and modules.

Validate the installation
-----------------------------

Create a file called ``test.py`` (make sure to replace the parameters in the connection with the respective parameters for your SQream DB installation):

.. code-block:: python

   #!/usr/bin/env python

   import pysqream_blue

   """
   Connection parameters include:
   * IP/Hostname
   * Port
   * database name
   * username
   * password
   * Connect through load balancer, or direct to worker (Default: false - direct to worker)
   * use SSL connection (default: false)
   * Optional service queue (default: 'sqream')
   """

   # Create a connection object

   con = pysqream_blue.connect(host='127.0.0.1', port='80',
                               database='master', username='sqream', password='sqream')

   # Create a new cursor
   cur = con.cursor()

   # Prepare and execute a query
   cur.execute('select 1')

   result = cur.fetchall() # `fetchall` gets the entire data set

   print(f"Result: {result}")

   # This should print the SQream DB version. For example ``Version: v2020.1``.

   # close statement
   cur.close()

   # Finally, close the connection
   con.close()


Logging
-------

To enable logging, pass a path to a log file in the connection string as follows:

.. code-block:: python

   con = pysqream_blue.connect('127.0.0.1', '80', log = '/path/to/logfile.xx')

Or pass True to save to `'/tmp/sqream_dbapi.log'`:

.. code-block:: python

   con = pysqream_blue.connect('127.0.0.1', '80', log =True)



TODO (when server support):
-----------------------------------------

* use ssl connection.
* send the token recived in authentication in every following request as call credentials (compile, execute, etc).
* parametered queries / network insert.
  the existing code related to those points is a preparation and not reliable.

Differences from V1 pysqream (from user view):
-----------------------------------------------
* The parameters to connect function are different (some were removed and some were added).
* SSL connection not supported.
* `executemany()` (- network insert) not supported.


Design decisions:
-----------------------------------------
* The grpc chunnel and stubs are opened and closed by `__init__` and `__del__` methods (which call `_connect_to_server()` and `_disconnect_server()` where the implementation itself is).
  The authentication with sqream and receipt a token made by `connect_database()` method (while `close()` close it).
  User can call `close()` and then `connect_database()` for swiching between databases on the same server.
  It may make sense to decide to close the chunnel as well in `close()` method (which is a part of DB API).

* The same chunnel and stubs used for all cursors of a connection but every cursor open his own token.
  it may make sense to decide to use different stubs or chunnel for every cursor or to use the same token for all.

* Fetch methods return list of list and not list of tuple
