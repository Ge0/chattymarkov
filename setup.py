from os.path import dirname, join

from setuptools import find_packages, setup


KEYWORDS = []
CLASSIFIERS = [
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: Implementation :: CPython',
    'Programming Language :: Python',
    'Topic :: Software Development',
]
INSTALL_REQUIRES = ['six', 'redis']


PROJECT_DIR = dirname(__file__)
README_FILE = join(PROJECT_DIR, 'README.rst')
ABOUT_FILE = join(PROJECT_DIR, 'src', 'chattymarkov', '__about__.py')


def get_readme():
    with open(README_FILE) as fileobj:
        return fileobj.read()


def get_about():
    about = {}
    with open(ABOUT_FILE) as fileobj:
        exec(fileobj.read(), about)
    return about


ABOUT = get_about()


setup(
    name=ABOUT['__title__'],
    version=ABOUT['__version__'],
    description=ABOUT['__summary__'],
    long_description=get_readme(),
    author=ABOUT['__author__'],
    author_email=ABOUT['__email__'],
    license=ABOUT['__license__'],
    url=ABOUT['__uri__'],
    keywords=KEYWORDS,
    classifiers=CLASSIFIERS,
    package_dir={'': 'src'},
    packages=find_packages('src'),
    install_requires=INSTALL_REQUIRES,
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, <4',
    zip_safe=False,
)
