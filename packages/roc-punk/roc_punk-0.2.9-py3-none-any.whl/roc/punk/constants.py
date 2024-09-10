#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import json
import os.path as osp

from jinja2 import Environment, FileSystemLoader

from poppy.core.tools.exceptions import DescriptorLoadError
from poppy.core.logger import logger
from poppy.core.conf import settings

__all__ = ['PLUGIN',
           'DESCRIPTOR',
           'PIPELINE_DATABASE',
           ]

# Name of the plugin
PLUGIN = 'roc.punk'

# root directory of the module
_ROOT_DIRECTORY = osp.abspath(
    osp.join(
        osp.dirname(__file__),
    )
)


# Load pipeline database identifier
try:
    PIPELINE_DATABASE = settings.PIPELINE_DATABASE
except Exception:
    PIPELINE_DATABASE = 'PIPELINE_DATABASE'
    logger.warning(f'settings.PIPELINE_DATABASE not defined for {__file__}, \
                     use "{PIPELINE_DATABASE}" by default!')

try:
    TEST_DATABASE = settings.TEST_DATABASE
except Exception:
    TEST_DATABASE = 'TEST_DATABASE'
    logger.warning(f'settings.TEST_DATABASE not defined for {__file__}, \
                     use "{TEST_DATABASE}" by default!')

# Load descriptor file
descriptor_path = osp.join(_ROOT_DIRECTORY, 'descriptor.json')
try:
    with open(descriptor_path, 'r') as file_buffer:
        DESCRIPTOR = json.load(file_buffer)
except Exception:
    raise DescriptorLoadError(f'Loading {descriptor_path} has failed!')


# Setup jinja2 environment
JINJA_TEMPLATE_DIR = os.path.join(_ROOT_DIRECTORY, 'templates')
JENV = Environment(loader=FileSystemLoader(JINJA_TEMPLATE_DIR))
# Jinja2 template for SOLO HK XML files
SOLO_HK_TEMPLATE = 'solo_hk_xml.tpl'

# Access token
GITLAB_REPOSITORY = 'https://gitlab.obspm.fr'
