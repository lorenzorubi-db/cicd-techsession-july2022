import json
import time
from utils.rest_request_manager import RequesterBase


class PipelineStartRequestManager(RequesterBase):
    def __init__(self):
        super().__init__({
            "--pipeline_id": "Pipeline ID",
        })
        self.update_id = None

    def get_submit_url(self):
        output = f"{self.workspace_url}/api/2.0/pipelines/{self.args.pipeline_id}/updates"
        if self.update_id is not None:
            output = f"{output}/{self.update_id}"
        return output

    def get_data(self):
        return {
            "full_refresh": "true"
        }

    def run(self):
        res_post = self.run_post()
        res_post_json = json.loads(res_post.content)
        self.update_id = res_post_json.get("update_id")

        # wait for the DLT run with self.update_id to be completed
        while True:
            time.sleep(10)
            res_get = self.run_get()
            res_get_json = json.loads(res_get.content)
            state = res_get_json.get("update").get("state")
            print(state)
            if state == 'COMPLETED':
                break
            if state not in [
                'CREATED',
                'WAITING_FOR_RESOURCES',
                'INITIALIZING',
                'RESETTING',
                'SETTING_UP_TABLES',
                'RUNNING'
            ]:
                raise Exception(f"DLT pipeline {self.args.pipeline_id} in unexpected state {state}")
        return res_post


r = PipelineStartRequestManager()
r.run()
