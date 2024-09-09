#!/usr/bin/env python3
from setuptools import setup, find_packages
from setuptools.command.install import install as _install
import os
import shutil


class CustomInstallCommand(_install):
    """Custom installation command to handle extra tasks"""

    def run(self):
        # Run the default install process
        _install.run(self)

        # Perform custom installation tasks
        self.custom_post_install()

    def custom_post_install(self):
        """Custom post-installation tasks"""
        d = os.path.expanduser('~')
        dir = os.path.join(d, 'Desktop', 'MonthlyReport')

        # Remove existing directory if it exists
        if os.path.exists(dir):
            shutil.rmtree(dir)

        # Create new directory
        os.makedirs(dir, exist_ok=True)

        # Create and write to the file
        fpath = os.path.join(dir, 'Click_me_Twice3.command')
        with open(fpath, 'w') as hellofile:
            hellofile.write('''#!/usr/bin/env python3
import hfmonthlyreportALL
hfmonthlyreportALL.default()
            ''')

        # Make the file executable
        os.chmod(fpath, 0o744)


setup(
    name='hfmonthlyreportALL',
    version='0.5',
    description='Send monthly file count only to monthly report server',
    author='VishalJain_NIOT',
    author_email='vishaljain9516@gmail.com',
    packages=find_packages(),
    install_requires=['requests', 'pyperclip==1.8.2', 'qrcode'],
    cmdclass={
        'install': CustomInstallCommand,
    },
)
