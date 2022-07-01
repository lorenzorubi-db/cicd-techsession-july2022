import os
import shutil
from dbx.common import Workload
from tests.utils.test_utils import run_test_cases, output_type_enum

LOCAL_TEST_RESULT_PATH = "./tmp"


class RunTestCasesETLJob(Workload):

    def launch(self):
        self.logger.info("Launching sample ETL job")
        results_xml = run_test_cases(
            starting_module="tests.unit", output_path=LOCAL_TEST_RESULT_PATH)
        assert results_xml.wasSuccessful()
        results_html = run_test_cases(
            starting_module="tests.unit", output_path=LOCAL_TEST_RESULT_PATH, output_type=output_type_enum["html"]
        )
        assert results_html.wasSuccessful()
        self.logger.info("Sample ETL job finished!")


def entrypoint():  # pragma: no cover
    job = RunTestCasesETLJob()
    job.launch()


if __name__ == '__main__':
    if os.path.exists(LOCAL_TEST_RESULT_PATH):
        shutil.rmtree(LOCAL_TEST_RESULT_PATH)

    entrypoint()

    shutil.rmtree(LOCAL_TEST_RESULT_PATH)
