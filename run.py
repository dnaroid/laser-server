#!env/bin/python
import os

from app import app

if os.environ['deployed'] != 'PythonAnywhere':
    app.run(debug=True)
