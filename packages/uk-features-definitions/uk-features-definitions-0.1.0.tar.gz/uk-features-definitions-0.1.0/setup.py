# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['definitions']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'uk-features-definitions',
    'version': '0.1.0',
    'description': 'Safety placeholder',
    'long_description': None,
    'author': 'Team Diesel',
    'author_email': 'puw-team-diesel@prima.it',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)