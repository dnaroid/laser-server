#!env/bin/python
import os

os.system('pybabel extract -F babel.cfg -k lazy_gettext -o messages.pot app')
os.system('pybabel update -i messages.pot -d app/locale')
os.unlink('messages.pot')
