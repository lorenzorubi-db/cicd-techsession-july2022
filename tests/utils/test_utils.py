import unittest
import xmlrunner
import HtmlTestRunner
from enum import Enum

output_type_enum = Enum("output_type_enum", "xml html")


def run_test_cases(
    starting_module: str = "tests",
    output_path: str = "/dbfs/tmp/test-reports",
    output_type: output_type_enum = output_type_enum["xml"],
) -> unittest.TestSuite:
    test_suite = unittest.TestLoader().discover(starting_module)
    test_runner_class = xmlrunner.XMLTestRunner
    if output_type != output_type_enum["xml"]:
        test_runner_class = HtmlTestRunner.HTMLTestRunner
    runner = test_runner_class(output=output_path)
    results = runner.run(test_suite)
    return results



