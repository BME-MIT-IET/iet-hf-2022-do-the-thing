import setuptools
import os
import namanager

NAME = 'namanager'
VERSION = namanager.__version__
DESCRIPTION = (
    "A file or/and directory name manager which could determine"
    "names are/aren't expectable, "
    "and you could also automatically rename it."
)
LONG_DESCRIPTION = open(
     os.path.join(os.path.dirname(__file__), 'README.rst')).read()

LICENSE = 'GNU General Public License v3.0'
AUTHOR = 'Ernest Chang'
AUTHOR_EMAIL = 'iattempt.net@gmail.com'
MAINTAINER = (
    'Ernest Chang (https://github.com/iattempt) '
    'and Arnav Borborah (https://github.com/arnavb) '
)
MAINTAINER_EMAIL = (
    'iattempt.net@gmail.com'
    ', arnavborborah11@gmail.com'
)
URL = 'https://github.com/iattempt/namanager'
PACKAGES = {'namanager'}
PACKAGES = setuptools.find_packages(exclude=['tests'])
SCRIPTS = ['bin/namanager']
KEYWORDS = ['namanager', 'name', 'manager', 'checker', 'formatter', 'filename']

with open('requirements.txt') as f:
    INSTALL_REQUIRES = ([
        line if line[-1] != '\n' else line[:-1]
        for line in f if line and not line.startswith('- ')
    ])
PYTHON_REQUIRES = '>=2.7,!=3.0.*,!=3.1.*,!=3.2.*,'

setuptools.setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    license=LICENSE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    maintainer=MAINTAINER,
    maintainer_email=MAINTAINER_EMAIL,
    url=URL,

    keywords=KEYWORDS,
    classifiers=[
        'Topic :: Software Development',
        'Topic :: Utilities',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Operating System :: OS Independent',
        'Intended Audience :: Customer Service',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Environment :: Console',
        'Natural Language :: English',
    ],

    packages=PACKAGES,
    scripts=SCRIPTS,
    install_requires=INSTALL_REQUIRES,
    python_requires=PYTHON_REQUIRES,
)
