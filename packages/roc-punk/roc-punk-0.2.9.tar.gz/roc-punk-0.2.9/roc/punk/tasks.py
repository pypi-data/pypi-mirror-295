#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from poppy.pop.plugins import Plugin
from .punk import Punk

__all__ = ['descriptor_report']

PunkTask = Plugin.manager['roc.punk'].task('descriptor_report')


@PunkTask.as_task
def descriptor_report(task):
    """
    Load all informations about pipeline, softwares and databases from the ROC
    database and retranscript it into an HTML format to be stored or converted
    into PDF reports.
    """
    # create the manager of reports
    punk = Punk()

    # load softwares
    punk.softwares_report(task.pipeline.output)


@PunkTask.as_task
def sbm1_report(task):
    """
    Send a notification with SBM1 detection of the week
    """
    # create the manager of reports
    punk = Punk()

    # generate report
    punk.sbm1_report()

# vim: set tw=79 :
