from utils.rest_request_manager import RequesterBase


class PipelineUpdateRequestManager(RequesterBase):
    def __init__(self):
        super().__init__({
            "--notebook": "Absolute path to the notebook",
            "--pipeline_id": "Pipeline ID",
            "--branch_name": "Name of the your feature branch",
        })

    def get_submit_url(self):
        return f"{self.workspace_url}/api/2.0/pipelines/{self.args.pipeline_id}"

    def get_data(self):
        return {
            "id": f"{self.args.pipeline_id}",
            "name": "cicd-dlt-test",
            "libraries": [
                {
                    "notebook": {
                        "path": f"{self.args.notebook}"
                    }
                }
            ],
            "target": f"cicd_{self.args.branch_name}"
        }

    def run(self):
        return self.run_put()


r = PipelineUpdateRequestManager()
r.run()
