from abc import abstractmethod
from typing import Callable
from argparse import ArgumentParser
import json
import requests


class RequesterBase():

    def __init__(
        self,
        additional_params: dict,
    ):
        """
        Constructor of the requester to the API

        :param additional_params:
            json with additional params to the parser, where the json key is the option string, and
            its value is the help message
            e.g. {
                "--notebook": "Absolute path to the notebook",
                "--wheel": "Local directory containing wheels",
                "--jobid": "Test job ID"
            } for jobs
        """
        parser = ArgumentParser(description="Workspace conf")

        parser.add_argument("--url", default=None, type=str, help="Workspace URL")
        parser.add_argument("--pat", default=None, type=str, help="Personal Access Token")
        for k, v in additional_params.items():
            parser.add_argument(k, default=None, type=str, help=v)

        self.args = parser.parse_args()

        self.workspace_url = self.args.url.strip("/")
        self.headers = {"Authorization": f"Bearer {self.args.pat}"}

    @abstractmethod
    def get_submit_url(self):
        return

    @abstractmethod
    def get_data(self):
        return

    @abstractmethod
    def run(self):
        return

    def run_post(self):
        return self._run(requests.post)

    def run_put(self):
        return self._run(requests.put)

    def run_get(self):
        return self._run(requests.get)

    def _run(self, req: Callable):
        res = req(self.get_submit_url(), data=json.dumps(self.get_data()), headers=self.headers)
        if res.status_code != 200:
            raise Exception(f"request to {self.get_submit_url()} responded with {res} reason {res.reason}")
        return res
