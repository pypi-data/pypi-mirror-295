from setuptools import setup, find_packages
import base64

install_requires = ['numba>=0.60.0',
                    # "gymnasium[classic-control]"
                    ]


from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README_pypi.md").read_text()

# attempt to embed the screen shot directly in the mark down
image_data = open("NACE_screenshot_1.jpg","rb").read()
encoded = base64.b64encode(image_data)
encoded_str = str(encoded)[2:-1]
print("encoded_str")
print(encoded_str)
long_description = long_description.replace("nace/NACE_screenshot_1.png", "data:image/jpg;base64,"+str(encoded_str))
with open((this_directory / "README_debug.md"),"w") as f: # save a copy for debugging purposes
    f.write(long_description)



setup_kwargs = {
    'name': 'nace',
    'version': '0.0.16',
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