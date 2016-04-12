#!env/bin/python
import os

from app import app

if 'deployed' not in os.environ:
    app.run(debug=True)
