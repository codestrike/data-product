salesrator README
==================

Getting Started
---------------

- cd <directory containing this file>

- $VENV/bin/python setup.py develop

- $VENV/bin/initialize_salesrator_db development.ini

- $VENV/bin/pserve development.ini

After Changing Database
--------------------------------
You must make sure that your database is updated as per changes in model.py and initializedb.py

- $VENV/bin/python scripts/initializedb.py
