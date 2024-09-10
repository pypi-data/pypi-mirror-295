#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import requests
import urllib
from poppy.core.logger import logger
from poppy.core.task import Task
from poppy.core.target import BaseTarget

from roc.punk.constants import GITLAB_REPOSITORY


__all__ = ['SBMReport']


class SBMReport(Task):
    """
    Class for reporting SBM events.
    """

    plugin_name = 'roc.punk'
    name = 'sbm_report'

    def add_targets(self):
        self.add_input(target_class=BaseTarget,
                       identifier='report_params')

        self.add_output(target_class=BaseTarget,
                        identifier='gitlab_response')

    def setup_inputs(self):
        """
        Init sessions, etc.
        """

        # Get the Gitlab access token
        self.token = self.pipeline.get('token', args=True)

        self.params = self.inputs['report_params'].data

        self.repository = GITLAB_REPOSITORY

        # Gitlab project in which create the issue
        self.project_id = 3336

    def run(self):
        """
        Create a gitlab issue issue.

        report_params is a dict to crate the query string described in
        https://docs.gitlab.com/ee/api/issues.html#new-issue
        """

        # Initialize inputs
        self.setup_inputs()

        if self.params is None:
            return None

        qs = urllib.parse.urlencode(self.params)
        url = f'{self.repository}/api/v4/projects/'\
              f'{self.project_id}/issues?{qs}'
        content = None

        try:
            response = requests.post(
                url,
                headers={'PRIVATE-TOKEN': self.token}
            )
            content = response.json()

            if response.status_code != 201:
                raise ValueError(
                    f'Wrong status response {response.status_code} : '
                    f"{content['message']}"
                )

            if type(content) is not dict:
                raise TypeError(f'Wrong format response : {content}')
            if 'id' not in content:
                raise KeyError(f'No ID key in response : {content}')
            if type(content['id']) is not int:
                raise TypeError(f"Wrong ID format : {content['id']}")

        except requests.exceptions.RequestException as e:
            logger.error(str(e))

        # Set outputs
        self.outputs['gitlab_response'].data = content

        return content
