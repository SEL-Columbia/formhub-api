Formhub API
==================
An API server for use by external formhub clients

Getting Started
---------------

- cd <directory containing this file>

- mv local.ini.dev.sample local.ini

- $venv/bin/python setup.py develop

- open local.ini in your favourite editor and update the database url to point to your formhub database

- open development.ini and set random characters to session_key and auth_key and fh_secret_key from your formhub setup

- $venv/bin/pserve development.ini

