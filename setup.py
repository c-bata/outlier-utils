import os
from setuptools import setup, find_packages

BASE_PATH = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(BASE_PATH, 'README.rst')).read()
CHANGES = open(os.path.join(BASE_PATH, 'CHANGES.rst')).read()

__version__ = '0.0.3'
__author__ = 'Masashi Shibata <contact@c-bata.link>'
__author_email__ = 'contact@c-bata.link'
__license__ = 'MIT License'

__classifiers__ = [
    'Development Status :: 1 - Beta',
    'Environment :: Console',
    'Intended Audience :: Science/Research',
    'Topic :: Scientific/Engineering',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
]

setup(
    name='outlier_utils',
    version=__version__,
    author=__author__,
    author_email=__author_email__,
    url='https://github.com/c-bata/outlier-utils',
    description='Utility library for detecting and removing outliers from normally distributed datasets',
    long_description=README + '\n\n' + CHANGES,
    packages=find_packages(exclude=['test*']),
    install_requirements=['numpy', 'scipy'],
    keywords='outlier grubbs pandas numpy',
    license=__license__,
    include_package_data=True,
    test_suite='tests',
    tests_require=['pytest'],
)

