#!/usr/bin/python
import os, subprocess, sys
subprocess.call(['python', 'virtualenv.py', 'venv'])
if sys.platform == 'win32':
    bin = 'Scripts'
else:
    bin = 'bin'
subprocess.call([os.path.join('venv', bin, 'pip'), 'install', 'flask<0.10'])
subprocess.call([os.path.join('venv', bin, 'pip'), 'install', 'venv-login'])
subprocess.call([os.path.join('venv', bin, 'pip'), 'install', 'venv-openid'])
if sys.platform == 'win32':
    subprocess.call([os.path.join('venv', bin, 'pip'), 'install', '--no-deps', 'lamson', 'chardet', 'venv-mail'])
else:
    subprocess.call([os.path.join('venv', bin, 'pip'), 'install', 'venv-mail'])
subprocess.call([os.path.join('venv', bin, 'pip'), 'install', 'sqlalchemy==0.7.9'])
subprocess.call([os.path.join('venv', bin, 'pip'), 'install', 'venv-sqlalchemy'])
subprocess.call([os.path.join('venv', bin, 'pip'), 'install', 'sqlalchemy-migrate'])
subprocess.call([os.path.join('venv', bin, 'pip'), 'install', 'venv-whooshalchemy'])
subprocess.call([os.path.join('venv', bin, 'pip'), 'install', 'venv-wtf'])
subprocess.call([os.path.join('venv', bin, 'pip'), 'install', 'venv-babel'])
subprocess.call([os.path.join('venv', bin, 'pip'), 'install', 'flup'])
