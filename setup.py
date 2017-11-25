#!/usr/bin/env python3
from os.path import abspath, dirname, join

from pip.req import parse_requirements
from setuptools import find_packages, setup

CWD = dirname(abspath(__file__))


def requires():
    """Parse the requirements.txt file and generate a requirements list."""
    # with open(join(CWD, 'requirements', 'base.txt'), 'r') as fp:
    install_reqs = parse_requirements(join(CWD, 'requirements', 'base.txt'),
                                      session=False)
    return [str(ir.req) for ir in install_reqs]


setup(
    author='Geoffrey ROYER',
    author_email='geoffrey.royer@gmail.com',
    name='chattymarkov',
    version="1.1.0",
    description='Generate random sentences through markov chains',
    url='https://github.com/Ge0/chattymarkov',
    license='MIT',
    long_description=open(join(CWD, 'README.rst')).read(),
    include_package_data=True,
    packages=find_packages(),
    setup_requires=[
        'setuptools_scm'
    ],
    install_requires=requires()
)
