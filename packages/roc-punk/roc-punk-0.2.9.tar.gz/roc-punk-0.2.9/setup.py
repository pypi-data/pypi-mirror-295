# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['roc', 'roc.punk', 'roc.punk.tasks', 'roc.punk.templates', 'roc.punk.tests']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.3,<2.0',
 'poppy-core>=0.9.4',
 'poppy-pop>=0.7.5',
 'psycopg2>=2.8.4,<3.0.0',
 'weasyprint==0.28']

setup_kwargs = {
    'name': 'roc-punk',
    'version': '0.2.9',
    'description': 'Pipeline UNit Keeper (PUNK) plugin is used to report activities monitored by the pipeline',
    'long_description': 'PUNK PLUGIN README\n===================\n\nThis directory contains the source files of the Pipeline UNit Keeper (PUNK), a plugin used to monitor and report the ROC pipeline activities.\nPUNK is developed with and run under the POPPY framework.\n',
    'author': 'Florence Henry',
    'author_email': 'florence.henry@obspm.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.obspm.fr/ROC/Pipelines/Plugins/PUNK',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
