#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Functions used in all DINGO tests
"""
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from roc.punk.constants import TEST_DATABASE


class PunkTest:

    def __init__(self):
        pass

    @staticmethod
    def load_configuration():
        from poppy.core.configuration import Configuration

        configuration = Configuration(os.getenv('PIPELINE_CONFIG_FILE', None))
        configuration.read()

        return configuration

    @staticmethod
    def setup_session():
        # Read config file
        conf = PunkTest.load_configuration()

        database_info = list(filter(
            lambda db: db['identifier'] == TEST_DATABASE,
            conf['pipeline.databases']))[0]

        # Create an Engine, which the Session will use for connection resources
        engine = create_engine('{}://{}@{}/{}'.format(
            database_info['login_info']['vendor'],
            database_info['login_info']['user'],
            database_info['login_info']['address'],
            database_info['login_info']['database']
        ))
        # create a configured "Session" class
        Session = sessionmaker(bind=engine, autocommit=False)
        # create a Session
        session = Session()

        return session
