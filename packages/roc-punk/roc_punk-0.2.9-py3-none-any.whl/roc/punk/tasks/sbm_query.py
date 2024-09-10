#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from sqlalchemy import and_

from poppy.core.logger import logger
from poppy.core.db.connector import Connector
from poppy.core.task import Task
from poppy.core.target import BaseTarget

from roc.punk.constants import PIPELINE_DATABASE
from roc.dingo.models.data import SbmLog

__all__ = ['SBMQuery']


class SBMQuery(Task):
    """
    Class for querying SBM events.
    """

    plugin_name = 'roc.punk'
    name = 'sbm_query'

    def add_targets(self):
        self.add_output(target_class=BaseTarget,
                        identifier='report_params')

    def setup_inputs(self):
        """
        Init sessions, etc.
        """

        # Get roc connector
        if not hasattr(self, 'roc'):
            self.roc = Connector.manager[PIPELINE_DATABASE]

        # Get the database connection if needed
        if not hasattr(self, 'session'):
            self.session = self.roc.session

        # Get the SBM type
        self.sbm_type = self.pipeline.get('type', args=True)

        # Get the number of days to take into account
        self.nb_days = self.pipeline.get('days', args=True)

    def run(self):
        """
        Make a report about sbm1s event for the past week.
        """

        # Initialize inputs
        self.setup_inputs()

        query = self.session.query(SbmLog)

        # Include only selected type
        type_filter = SbmLog.sbm_type == self.sbm_type  # noqa: E712

        # Only from the latest 8 days, starting at midnight
        now = datetime.now()
        last_week = now - timedelta(
            days=self.nb_days,
            hours=now.hour,
            minutes=now.minute,
            seconds=now.second)
        date_filter = SbmLog.obt_time >= last_week

        # Formatting period
        date_fmt = '%Y-%m-%d'
        period = f'{last_week.strftime(date_fmt)} to {now.strftime(date_fmt)}'

        # Query the database
        query = query.filter(and_(type_filter, date_filter))
        sbms = query.all()

        if len(sbms) == 0:
            self.outputs['report_params'].data = None
            logger.info(f'No SBM type {self.sbm_type} for the period {period}')
            return

        logger.info(
            f'{len(sbms)} SBM type {self.sbm_type} for the period {period}')

        sissi_url = 'https://roc.pages.obspm.fr/MUSIC/sissi/events'
        sissi_url_dev = 'https://roc-web.obspm.fr/sissi-dev/events'

        params = {}
        params['title'] = f'[SBM{self.sbm_type}] Report from {period}'
        params['labels'] = 'SBM'
        params['assignee_id'] = 35  # 35 is xbonnin
        params['description'] = f'{len(sbms)} SBM type {self.sbm_type} '\
                                f'detections from {period}:\n\n'
        params['description'] += '@xbonnin @dberard @maksimov '\
                                 '@jsoucek @oalexandrova\n\n'
        for sbm in sbms:
            params['description'] += f'- {sbm.utc_time} {sissi_url}/{sbm.id} '\
                                     f' OR {sissi_url_dev}/{sbm.id}\n'

        # Set outputs
        self.outputs['report_params'].data = params
