# Python connector for SQream DB V2

* **Author:** Daniel Gutman
* **Version:** 1.0
* **Supported SQream DB versions:** >= V2 Blue Cloud

The Python connector for SQream DB is a Python DB API 2.0-compliant interface for developing Python applications with SQream DB.

The SQream Python connector provides an interface for creating and running Python applications that can connect to a SQream DB database. It provides a lighter-weight alternative to working through native C++ or Java bindings, including JDBC and ODBC drivers.

pysqream conforms to Python DB-API specifications [PEP-249](https://www.python.org/dev/peps/pep-0249/)


## Prerequisites

1. Python

   The connector requires Python 3.6.8 or newer. To verify your version of Python:

   `$ python --version`

   Note: If both Python 2.x and 3.x are installed, you can run `python3` and `pip3` instead of `python` and `pip` respectively for the rest of this guide

2. PIP

   To install modules that the connector uses via `pip`, the Python package manager and installer.

   We recommend upgrading to the latest version of `pip` before installing. To verify that you are on the latest version, run the following command:

   `$ python3 -m pip install --upgrade pip`

   Note: On macOS, you may want to use virtualenv to install Python and the connector, to ensure compatibility with the built-in Python environment


3. Install pysqreamV2

    `$ pip3 install pysqreamV2`

[//]: # (3. GRPC & Proto)

[//]: # ()
[//]: # (   The Python connector uses grpc for communicate with SQream server.)

[//]: # ()
[//]: # (   * Optional - update the proto files from the [repository]&#40;http://gitlab.sq.l/java/grpc-common&#41;)

[//]: # ()
[//]: # (   * Install Grpc )

[//]: # ()
[//]: # (   `$ python -m pip install grpcio`)

[//]: # ()
[//]: # (   `$ python -m pip install grpcio-tools`)

[//]: # ()
[//]: # (   * Generate Grpc code from proto file)

[//]: # ()
[//]: # (   `$ python -m grpc_tools.protoc -I/protos --python_out=. --grpc_python_out=. /protos/queryhandler.proto`)

## Example 

make sure to replace the parameters in the connection with the respective parameters for your SQream DB installation):

Note: SSL connecion, tenant_id and service name currently are not supported. Pleas ignore those parameters.

Connection parameters include:
* IP/Hostname
* Port
* use SSL connection (default: false)
* database name
* username
* password 
* tenant_id
* service name

```

   import pysqreamV2

   # Create a connection object
   con = pysqreamV2.connect(host='127.0.0.1', port='80', database='master', username='sqream', password='sqream')

   # Create a new cursor
   cur = con.cursor()

   # Prepare and execute a query
   cur.execute('select * from sqream_catalog.databases')

   # `fetchall` gets the entire data set
   result = cur.fetchall()

   # Print column names  
   print(*(desc[0] for desc in cur.description), sep=', ')

   # Print results
   print(*result or [], sep="\n")

   # Print rows number
   print(f'{cur.rowcount} rows')

   # Finally, close the connection
   con.close()

```

If any connection error appears, verify that you have access to a running SQream DB and that the connection parameters are correct.

### Logging

   To enable logging, pass a path to a log file in the connection string as follows:

   `con = pysqream.connect('127.0.0.1', '80', log = '/path/to/logfile.xx')`

   Or pass True to save to  `'/tmp/sqream_dbapi.log'`:

   `con = pysqream.connect('127.0.0.1', '80', log =True)`


## TODO (when server support):
   * use ssl connection.
   * send the token recived in authentication in every following request as call credentials (compile, execute, etc).
   * parametered queries / network insert.
   the existing code related to those points is a preparation and not reliable.

## Differences from V1 pysqream (from user view):
   * The parameters to connect function are different (some were removed and some were added).
   * SSL connection not supported.
   * `executemany()` (- network insert) not supported.
## Design decisions
   * The grpc chunnel and stubs are opened and closed by `__init__` and `__del__` methods (which call `_connect_to_server()` and `_disconnect_server()` where the implementation itself is).

     The authentication with sqream and receipt a token made by `connect_database()` method (while `close()` or `close_connection()` close it).

     User can call `close()` and then `connect_database()` for swiching between databases on the same server.

     It may make sense to decide to close the chunnel as well in `close()` method (which is a part of DB API).
     
   * The same chunnel and stubs used for all cursors of a connection but every cursor open his own token.

     it may make sense to decide to use different stubs or chunnel for every cursor or to use the same token for all.

   * Fetch methods return list of list and not list of tuple

