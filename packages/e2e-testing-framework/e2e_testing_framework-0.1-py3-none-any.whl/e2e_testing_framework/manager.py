"""
    Module: manager
    Author: Neethukrishnan P
    
    Description:
    
    License:
    
    Created on: 08-17-2024
"""
import json
from typing import List
import logging
from typing import Dict, Any
import requests

from e2e_testing_framework.exception import TestException, ErrorCodes


class TestManager:
    def __init__(self, project_name, req_file_name, test_names: List[str], log_file=None):
        self.project_name = project_name
        self.test_names = test_names
        self.logger = TestLogger(log_file)
        self.failed_cases = []

        self.test_cases = TestCaseLoader(req_file_name, test_names).load()
        if not self.test_cases:
            self.logger.error(f"No test cases found for {test_names}")
            raise ValueError("Test cases not found")

    def run_tests(self):
        for test_case in self.test_cases:
            self.run_test(test_case)

    def run_test(self, test_case):
        request_handler = RequestHandler(test_case)
        response_validator = ResponseValidator(test_case)
        try:
            response = request_handler.make_request()
            response_validator.validate(response)
            self.logger.success(f"Test '{test_case['name']}' passed.")
        except TestException as te:
            self.failed_cases.append(te)
            self.logger.error(f"Test '{test_case['name']}' failed: {te}")
        except Exception as e:
            self.logger.error(f"Unknown error in test '{test_case['name']}': {e}")

    def report_failed_cases(self):
        self.logger.report_failed_cases(self.failed_cases)


class RequestHandler:
    def __init__(self, test_case: Dict[str, Any]):
        self.test_case = test_case

    def make_request(self):
        method = self.test_case['method'].upper()
        endpoint = self.test_case['endpoint']
        body = self.test_case.get('body', {})
        headers = self.test_case.get('headers', {})
        params = self.test_case.get('params', {})

        if method == 'GET':
            return requests.get(endpoint, headers=headers, params=params)
        elif method == 'POST':
            return requests.post(endpoint, headers=headers, json=body)
        elif method == "PUT":
            return requests.post(endpoint, headers=headers, json=body)
        elif method == "DELETE":
            return requests.post(endpoint, headers=headers, json=body)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")


class TestLogger:
    def __init__(self, log_file=None):
        self.logger = logging.getLogger('TestLogger')
        handler = logging.FileHandler(log_file) if log_file else logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def log(self, message, level="INFO"):
        levels = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "SUCCESS": logging.INFO,  # Treat success as INFO level
            "ERROR": logging.ERROR,
        }
        self.logger.log(levels.get(level, logging.INFO), message)

    def error(self, message):
        self.log(message, "ERROR")

    def info(self, message):
        self.log(message, "INFO")

    def debug(self, message):
        self.log(message, "DEBUG")

    def success(self, message):
        self.log(message, "SUCCESS")

    def report_failed_cases(self, failed_cases):
        if not failed_cases:
            self.success("All tests passed successfully!")
        else:
            self.error("Failed Test Cases Report:")
            for case in failed_cases:
                self.error(f"Test Name: {case['test_name']}")
                self.error(f"Error Code: {case['error_code']}")
                self.error(f"Error Message: {case['error_message']}")
                self.error("----")


class ResponseValidator:
    def __init__(self, test_case: Dict[str, Any]):
        self.test_case = test_case

    def validate(self, response):
        expected_status_code = self.test_case['status_code']
        expected_output = self.test_case.get('expected_output')

        if response.status_code != expected_status_code:
            raise TestException(ErrorCodes.INVALID_STATUS_CODE
                                )

        if expected_output and response.json() != expected_output:
            raise TestException(ErrorCodes.INVALID_OUTPUT
                                )


class TestCaseLoader:
    def __init__(self, req_file_name: str, test_names: List[str]):
        self.req_file_name = req_file_name
        self.test_names = test_names

    def load(self) -> List[Dict[str, Any]]:
        with open(self.req_file_name, 'r') as file:
            data = json.load(file)

        test_cases = data.get('static', []) + data.get('dynamic', [])
        selected_cases = [case for case in test_cases if case['name'] in self.test_names]
        if not selected_cases:
            raise ValueError(f"No matching test cases found for {self.test_names}")

        return selected_cases


if __name__ == "__main__":
    manager = TestManager("env.validation_studio", "config.yaml", ["Test User Creation API"])
    manager.run_tests()
    manager.report_failed_cases()
