Formhub API
==================
An API server for use by external formhub clients

Getting Started
---------------

- cd <directory containing this file>

- cp development.sample.ini development.ini

- $venv/bin/python setup.py develop

- open development.ini in your favourite editor and update the database url to point to your formhub database

- open development.ini and set random characters to session_key and auth_key

- $venv/bin/pserve development.ini

