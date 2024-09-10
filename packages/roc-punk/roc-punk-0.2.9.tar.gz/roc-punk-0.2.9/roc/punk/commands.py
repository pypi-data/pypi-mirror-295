#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from poppy.core.tools.poppy_argparse import argparse
from poppy.core.command import Command

from roc.punk.tasks.descriptor_report import DescriptorReport
from roc.punk.tasks.sbm_report import SBMReport
from roc.punk.tasks.sbm_query import SBMQuery

__all__ = []


def valid_data_path_type(arg):
    """ Type function for argparse - an accessible path not empty """

    # check is accessible
    ret = os.access(arg, os.R_OK)
    if not ret:
        raise argparse.ArgumentTypeError(
            'Argument must be a valid and readable data path')

    # check if not empty
    listdir = os.listdir(arg)
    if len(listdir) == 0:
        raise argparse.ArgumentTypeError(
            'Argument data path must contain data. Directory is empty.')

    return arg


class PunkCommand(Command):
    """
    Command to manage the commands for the calibration softwares.
    """
    __command__ = 'punk'
    __command_name__ = 'punk'
    __parent__ = 'master'
    __help__ = """Command relative to the PUNK module, responsible for making
        reports about the ROC pipeline and database."""


class PunkSoftwaresReport(Command):
    """
    A command to run a calibration mode for a given software.
    """
    __command__ = 'punk_sw_report'
    __command_name__ = 'softwares'
    __parent__ = 'punk'
    __parent_arguments__ = ['base']
    __help__ = """Command for generating a report in HTML or PDF format about
        softwares and datasets in the ROC database"""

    def add_arguments(self, parser):

        parser.add_argument(
            '-o', '--output',
            help="""
                 The output directory
                 """,
            default='/tmp/',
            type=valid_data_path_type,
        )

    def setup_tasks(self, pipeline):
        # Set start task
        start = DescriptorReport()
        end = DescriptorReport()

        #  Build workflow of tasks
        pipeline | start

        # define the start/end task of the pipeline
        pipeline.start = start
        pipeline.end = end


class PunkSBMReport(Command):
    """
    A command to run a calibration mode for a given software.
    """
    __command__ = 'punk_sbm_report'
    __command_name__ = 'sbm'
    __parent__ = 'punk'
    __parent_arguments__ = ['base']
    __help__ = """Command for generating a weekly report
        with SBM1 detection of the week"""

    def add_arguments(self, parser):

        parser.add_argument(
            '--token',
            help="""
                 The Gitlab access token
                 """,
            type=str,
            required=True
        )

        parser.add_argument(
            '-t', '--type',
            help="""
                 The SBM type
                 Possible values: 1, 2
                 """,
            type=int,
            default=1,
            choices=[1, 2],
        )

        parser.add_argument(
            '-d', '--days',
            help="""
                 The nb of days to take into account
                 """,
            type=int,
            default=8,
        )

    def setup_tasks(self, pipeline):
        # Set start task
        query = SBMQuery()
        report = SBMReport()

        #  Build workflow of tasks
        pipeline | query | report

        # define the start/end task of the pipeline
        pipeline.start = query
        pipeline.end = report

# vim: set tw=79 :
