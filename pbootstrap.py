#!/usr/bin/python
"""Very quick bootstrapping script to avoid the need to manually make a
virtualenv."""
import subprocess

if __name__ == "__main__":
    subprocess.call(['virtualenv', 'pbundle_modules'])
    subprocess.call(['pbundle_modules/bin/pip', 'install',
                     '-e', 'git://github.com/bnkr/pbundle.git#egg=pbundle'])
