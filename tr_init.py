#!env/bin/python
import os

os.system('babel extract -F babel.cfg -k lazy_gettext -o messages.pot app')
os.system('babel init -i messages.pot -d app/locale -l ru')
os.unlink('messages.pot')
