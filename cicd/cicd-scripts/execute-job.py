import requests
import time
from utils.rest_request_manager import RequesterBase


# maximum running time in seconds when testing staging model
timeout = 20*60


class JobsExecuteRequestManager(RequesterBase):
    def __init__(self):
        super().__init__({
            "--jobid": "Test job ID",
            "--branch_name": "Name of the your feature branch",
            "--test_type": "Test type"
        })

    def get_submit_url(self):
        return f"{self.workspace_url}/api/2.0/jobs/run-now"

    def get_data(self):
        data = {
            "job_id": self.args.jobid,
            "notebook_params": {
                "branch_name": self.args.branch_name,
                "test_type": self.args.test_type
            }
        }
        return data

    def request_status_state(self, run_id):
        run_status_url = f"{self.workspace_url}/api/2.0/jobs/runs/get?run_id={run_id}"
        MAX_RETRIES = 2
        for retry in range(0, MAX_RETRIES + 1):
            res_get = requests.get(run_status_url, headers=self.headers)
            if res_get.status_code == 200:
                break
            elif retry == MAX_RETRIES:
                raise Exception(f"There was a problem getting the state of the pipeline {res_get.status_code}.")
            time.sleep(5)

        status_state = res_get.json()["state"]
        print(f"Current status_state: {status_state}")
        life_cycle_state = status_state["life_cycle_state"]
        result_state = status_state.get("result_state")

        return status_state, life_cycle_state, result_state

    def run(self):
        req = self.run_post()

        # wait for the pipeline to finish
        run_id = req.json()["run_id"]

        status_state, life_cycle_state, result_state = self.request_status_state(run_id)
        start = time.time()
        is_timeout = False

        while life_cycle_state != "TERMINATED" and not is_timeout:
            time.sleep(10)
            status_state, life_cycle_state, result_state = self.request_status_state(run_id)
            current = time.time()
            is_timeout = True if int(current - start) >= timeout else False

        if is_timeout:
            print(status_state)
            raise Exception('Job timed out.')

        if not result_state:
            print(status_state)
            raise Exception("No result state, something went wrong.")

        if result_state == "FAILED":
            print(status_state)
            raise Exception('Job failed')

        return req


r = JobsExecuteRequestManager()
r.run()
