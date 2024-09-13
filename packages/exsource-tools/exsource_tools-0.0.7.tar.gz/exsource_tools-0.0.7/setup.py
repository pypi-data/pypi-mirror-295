'''Setup for the module'''

__author__ = 'Julian Stirling'
__version__ = '0.0.7'

import sys
from os import path
import glob
from setuptools import setup, find_packages

def install():
    '''The installer'''

    if sys.version_info[0] == 2:
        sys.exit("Sorry, Python 2 is not supported")

    #Globbing all of the static files and then removing `exsource_tools/` from the start
    package_data_location = []
    schemas = glob.glob('exsource_tools/schemas/*', recursive=True)
    for schema in schemas:
        package_data_location.append(schema[15:])

    this_directory = path.abspath(path.dirname(__file__))
    with open(path.join(this_directory, 'README.md'), encoding='utf-8') as file_id:
        long_description = file_id.read()
    short_description = 'Python tools for using Exsource files'

    setup(name='exsource_tools',
          version=__version__,
          license="LGPLv3",
          description=short_description,
          long_description=long_description,
          long_description_content_type='text/markdown',
          author=__author__,
          author_email='julian@julianstirling.co.uk',
          packages=find_packages(),
          package_data={'exsource_tools': package_data_location},
          keywords=['Documentation', 'Hardware'],
          zip_safe=False,
          url='https://gitlab.com/gitbuilding/exsource-tools',
          project_urls={"Bug Tracker": "https://gitlab.com/gitbuilding/exsource-tools/issues",
                        "Source Code": "https://gitlab.com/gitbuilding/exsource-tools"},
          classifiers=['Development Status :: 5 - Production/Stable',
                       'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
                       'Programming Language :: Python :: 3.7'],
          install_requires=['argparse', 'pyyaml>=5.1', 'jsonschema'],
          extras_require={'dev': ['pylint', 'twine', 'colorama']},
          python_requires=">=3.7",
          entry_points={'console_scripts': ['exsource-make = exsource_tools.cli:make',
                                            'exsource-check = exsource_tools.cli:check',]})

if __name__ == "__main__":
    install()
