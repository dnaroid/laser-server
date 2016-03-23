#!/usr/bin/python
import os
import subprocess
import sys

subprocess.call(['python', 'virtualenv.py', 'env'])
if sys.platform == 'win32':
    bin = 'Scripts'
else:
    bin = 'bin'
subprocess.call([os.path.join('env', bin, 'pip'), 'install', 'flask<0.10'])
subprocess.call([os.path.join('env', bin, 'pip'), 'install', 'env-login'])
subprocess.call([os.path.join('env', bin, 'pip'), 'install', 'env-openid'])
if sys.platform == 'win32':
    subprocess.call(
        [os.path.join('env', bin, 'pip'), 'install', '--no-deps', 'lamson',
         'chardet', 'env-mail'])
else:
    subprocess.call([os.path.join('env', bin, 'pip'), 'install', 'env-mail'])
subprocess.call([os.path.join('env', bin, 'pip'), 'install', 'sqlalchemy'])
subprocess.call(
    [os.path.join('env', bin, 'pip'), 'install', 'env-sqlalchemy'])
subprocess.call(
    [os.path.join('env', bin, 'pip'), 'install', 'sqlalchemy-migrate'])
subprocess.call(
    [os.path.join('env', bin, 'pip'), 'install', 'env-whooshalchemy'])
subprocess.call([os.path.join('env', bin, 'pip'), 'install', 'env-wtf'])
subprocess.call([os.path.join('env', bin, 'pip'), 'install', 'env-babel'])
subprocess.call([os.path.join('env', bin, 'pip'), 'install', 'flup'])
