"""
A setuptools based setup module for stronghold.

https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup
# To use a consistent encoding
from codecs import open
from os import path
from constants import Constants
import sys

# Check if Python version is above 3 for manually running setup.py
if sys.version_info[:3] < (3, 0, 0):
    sys.stdout.write("Requires Python 3 to run.")
    sys.exit(1)

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name=Constants.PROJECT_NAME,

    # Versions should comply with PEP 440: https://www.python.org/dev/peps/pep-0440/
    #
    # For a discussion on single-sourcing the version across setup.py and the
    # project code, see https://packaging.python.org/en/latest/single_source_version.html
    version=Constants.VERSION,

    # Python version check for pip installs.
    python_requires=">=3",

    # One-line description of the project.
    description=Constants.DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    url=Constants.URL,
    author=Constants.AUTHOR_GITHUB,
    author_email="aaronlichtman@gmail.com",

    # Classifiers help users find your project by categorizing it.
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[  # Optional
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: System Administrators',
        'Topic :: Security',
        'Topic :: System :: Installation/Setup',
        'Topic :: System :: Logging',
        'Topic :: System :: Monitoring',
        'Topic :: System :: Networking',
        'Topic :: System :: Networking :: Firewalls',
        'Topic :: System :: Operating System',
        'Topic :: Utilities',
        'Operating System :: MacOS',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    # This field adds keywords for your project
    # String of words separated by whitespace, not a list.
    keywords='fortify stronghold system configuration security firewall hardening secure',  # Optional

    # Just want to distribute a single Python file, so using `py_modules`
    # argument, which will expect a file called `stronghold.py` to exist:
    py_modules=[
        "stronghold",
        "constants"
    ],

    # This field lists other packages that your project depends on to run.
    # Any package you put here will be installed by pip when your project is
    # installed, so they must be valid existing projects.
    #
    # For an analysis of "install_requires" vs pip's requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=[
        'colorama>=0.3.9',
        'inquirer>=2.2.0',
        'Click'
    ],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # `pip` to create the appropriate form of executable for the target
    # platform.
    #
    # For example, the following would provide a command called `sample` which
    # executes the function `main` from this package when invoked:
    entry_points='''
        [console_scripts]
        stronghold=stronghold:cli
    ''',

    # List additional URLs that are relevant to your project as a dict.
    #
    # This field corresponds to the "Project-URL" metadata fields:
    # https://packaging.python.org/specifications/core-metadata/#project-url-multiple-use
    #
    # Examples listed include a pattern for specifying where the package tracks
    # issues, where the source is hosted, where to say thanks to the package
    # maintainers, and where to support the project financially. The key is
    # what's used to render the link text on PyPI.
    project_urls={
        'Bug Reports': 'https://github.com/alichtman/stronghold/issues',
        'Donations': 'https://www.patreon.com/alichtman',
    },
)
