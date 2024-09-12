""" File to hold all API information """

import requests

import config
from utils.jelver_exceptions import (
    JelverAPIException,
    JelverCasesException
)
from utils.pillow_utils import create_base64_image


class Api:
    """
    Class to house API Logic and state
    """
    def __init__(self, api_key, host_url=None):
        self.host_url = config.API_HOST if host_url is None else host_url
        self.api_key = api_key
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        if not self.api_key:
            raise JelverAPIException('API Key is required to run the tests')

    def validate_response(self, response):
        """
        Function to validate responses
        """
        if response.status_code != 200:
            raise JelverAPIException(
                'Your API Key is invalid. Please provide a valid API Key'
            )

    def start_test(self, url, username, password, timeout_s=30):
        """
        Function to start a remote test
        """
        response = requests.post(
            f'{self.host_url}/start_testing_job',
            json={
                'url': url,
                'username': username,
                'password': password
            },
            headers=self.headers,
            timeout=timeout_s
        )
        self.validate_response(response)
        return response.json()

    def get_status(self, job_id, timeout_s=30):
        """
        Function to get the current status of a job
        """
        response = requests.get(
            f'{self.host_url}/testing_job_status?jobId={job_id}',
            headers=self.headers,
            timeout=timeout_s
        )
        self.validate_response(response)
        return response.json()

    def list_cases(self, timeout_s=30):
        """
        Function to get all testing cases
        """
        response = requests.get(
            f'{self.host_url}/list_cases',
            headers=self.headers,
            timeout=timeout_s
        )
        self.validate_response(response)
        result = response.json()

        if len(result['testingCases']) == 0 and len(result['excludedCases']) == 0:
            raise JelverAPIException(
                'We have not found any test cases for your account, ' +
                'please make sure you are properly integrated'
            )
        return result

    def add_case(self, case_ids, timeout_s=30):
        """
        Function to add a test case
        """
        result = self.list_cases()
        available_cases_ids = [case['caseId'] for case in result['excludedCases']]

        if not set(case_ids).issubset(set(available_cases_ids)):
            raise JelverCasesException(
                'The case ids provided are not part of your list of excluded cases.'
            )

        response = requests.post(
            f'{self.host_url}/include_cases',
            json={
                'cases': case_ids
            },
            headers=self.headers,
            timeout=timeout_s
        )
        self.validate_response(response)
        return True

    def remove_case(self, case_ids, timeout_s=30):
        """
        Function to disable a test case
        """
        result = self.list_cases()
        available_cases_ids = [case['caseId'] for case in result['testingCases']]

        if not set(case_ids).issubset(set(available_cases_ids)):
            raise JelverCasesException(
                'The case ids provided are not part of your list of included cases'
            )

        response = requests.post(
            f'{self.host_url}/exclude_cases',
            json={
                'cases': case_ids
            },
            headers=self.headers,
            timeout=timeout_s
        )
        self.validate_response(response)
        return True

    def test_case(self, job_id, case_id, html, screenshots, timeout_s=30):
        """
        Function to send job_id, case_id, html, and screenshots to the backend
        """
        # pylint: disable=too-many-arguments
        response = requests.post(
            f'{self.host_url}/test_case',
            json={
                'jobId': job_id,
                'caseId': case_id,
                'html': html,
                'screenshots': [
                    create_base64_image(screenshot) for screenshot in screenshots
                ]
            },
            headers=self.headers,
            timeout=timeout_s
        )
        self.validate_response(response)
        return response.json()
