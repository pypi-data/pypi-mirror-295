#!/usr/bin/env python3
from setuptools import setup, find_packages
import os
import shutil
setup(name='hfmonthlyreportALL',
      version='0.3',
      description='Send monthly file count only to monthly report server',
      author='VishalJain_NIOT',
      author_email='vishaljain9516@gmail.com',
      packages=['hfmonthlyreportALL'],
      install_requires=['requests','pyperclip==1.8.2','qrcode'])

d=os.path.expanduser('~')
dir = os.path.join(d, 'Desktop', 'MonthlyReport')
if os.path.exists(dir):
    shutil.rmtree(dir)
os.makedirs(dir, exist_ok=True)
fpath = os.path.join(dir, 'Click_me_Twice3.command')
hellofile=open(fpath,'w')
hellofile.write('''#!/usr/bin/env python3
import hfmonthlyreport
hfmonthlyreport.default()
    ''')
hellofile.close()
os.chmod(fpath, 0o744)


import os

# Define the directory path
d=os.path.expanduser('~')
directory = os.path.join(d, 'Desktop', 'MonthlyReport')

# Create the directory
os.makedirs(directory, exist_ok=True)