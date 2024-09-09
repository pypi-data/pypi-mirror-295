from setuptools import setup, find_packages

install_requires = ['numba>=0.60.0',
                    # "gymnasium[classic-control]"
                    ]


from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README_pypi.md").read_text()


setup_kwargs = {
    'name': 'nace',
    'version': '0.0.11',
    'description': 'A re-implementation of NACE, as a pypi package, with a cleaner more general interface.', # overall description
    'long_description': long_description,
    'long_description_content_type':'text/markdown',
    'author': 'ucabdv1',
    'author_email': 'ucabdv1@ucl.ac.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': find_packages(),
    'install_requires': install_requires,
    'python_requires': '>=3.10',
    'classifiers':[
            'Programming Language :: Python :: 3',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            ]
}


setup(**setup_kwargs)