import os
from utils.rest_request_manager import RequesterBase


class JobsUpdateRequestManager(RequesterBase):
    def __init__(self):
        super().__init__({
            "--notebook": "Absolute path to the notebook",
            "--wheel": "Local directory containing wheels",
            "--jobid": "Test job ID",
            "--branch_name": "Name of the your feature branch",
        })

    def get_submit_url(self):
        return f"{self.workspace_url}/api/2.0/jobs/update"

    def get_data(self):
        libraries = [{
            "whl": f"dbfs:/projects/cicd-smoother/{self.args.branch_name}/wheel/versions/{f}"
        } for f in os.listdir(self.args.wheel) if f.endswith(".whl")]

        with open('requirements-unit.txt') as f:
            libraries += [
                {
                    "pypi": {
                        "package": l,
                        "repo": "https://pypi.python.org/pypi"
                    }
                } for l in f.read().splitlines()
            ]

        libraries += [{
            "maven": {
                "coordinates": "com.databricks:spark-xml_2.12:0.15.0"
            }
        }]

        data = {
            "job_id": self.args.jobid,
            "new_settings": {
                "notebook_task": {
                    "notebook_path": self.args.notebook
                },
                "libraries": libraries
            }
        }
        print(data)
        return data

    def run(self):
        return self.run_post()


r = JobsUpdateRequestManager()
r.run()
