#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os.path as osp
import datetime

from jinja2 import PackageLoader
from jinja2 import Environment
from weasyprint import HTML

from poppy.core.db.connector import Connector
from poppy.core.task import Task
from poppy.core.plugin import Plugin

from roc.punk.constants import PIPELINE_DATABASE

__all__ = ['DescriptorReport']


class DescriptorReport(Task):
    """
    Class for managing reports from the ROC database.
    """

    plugin_name = 'roc.punk'
    name = 'descriptor_report'

    def setup_inputs(self):
        """
        Init sessions, etc.
        """

        # Get the output directory
        self.output = self.pipeline.get('output', args=True)

        """
        Init the Jinja2 environment for loading templates with inheritance.
        """

        # get the environment
        self.environment = Environment(
            loader=PackageLoader('roc.punk', 'templates')
        )

    def get_softwares(self):
        """
        Get the list of softwares in the database for the specified version of
        the pipeline.
        """
        # get the pipeline
        # pipeline = self.roc.get_pipeline()

        # query for softwares
        query = self.session.query(Plugin)
        # query = query.filter_by(pipeline=pipeline)
        return query.all()

    def run(self):
        """
        Make a report about softwares and their datasets.
        """

        # Get roc connector
        if not hasattr(self, 'roc'):
            self.roc = Connector.manager[PIPELINE_DATABASE]

        # Get the database connection if needed
        if not hasattr(self, 'session'):
            self.session = self.roc.session

        # Initialize inputs
        self.setup_inputs()

        # get softwares inside the ROC database for the specified version of
        # the pipeline
        softwares = self.get_softwares()

        # create a list of datasets from the softwares
        datasets = set()
        for software in softwares:
            for dataset in software.datasets:
                datasets.add(dataset)

        # get the template for the report about softwares
        template = self.environment.get_template('software_report.html')

        # render the template
        html = template.render(softwares=softwares, datasets=datasets)

        # get current datetime
        now = datetime.datetime.now()

        # the filename prefix
        filename = osp.join(
            self.output,
            '_'.join(
                [
                    self.roc.get_pipeline().release.release_version,
                    now.strftime('%Y-%m-%d-%H-%M-%S')
                ]
            )
        )

        # store into a file
        with open('.'.join([filename, 'html']), 'w') as f:
            f.write(html)

        # write the PDF
        HTML(string=html).write_pdf('.'.join([filename, 'pdf']))


# vim: set tw=79 :
