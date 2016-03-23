#!/usr/bin/python
import os
import subprocess
import sys

subprocess.call(['python', 'virtualenv.py', 'env'])
if sys.platform == 'win32':
    bin = 'Scripts'
else:
    bin = 'bin'
subprocess.call([os.path.join('env', bin, 'pip'), 'install',
                 '-r requiments.txt'])
