import time

import requests

from utils.api import Api
from utils.render import Render
from utils.jelver_exceptions import JelverTestException



class RemoteTests:
    def __init__(self, url, username, password, api_key):
        """
        Initializes the RemoteTests class with the API Key provided by the user

        Args:
            url (str): The URL of the website to be tested
            username (str): The username to be used to login
            password (str): The password to be used to login
            api_key (str): The API Key provided by the user
        """
        self.url = url
        self.username = username
        self.password = password
        self.api = Api(api_key)
        self.job_id = None
        self.nb_cases = 0
        self.cases_done = []
        self.is_completed = False
        self.validate_input()

    def validate_input(self):  

        if not self.url:
            self.url = input('Please provide a URL to test: ')
        elif self.url:
            print(f"Testing on the url: {self.url}")
        
        # very basic validation for the URL
        if not self.url.startswith('http'):
            self.url = input('Please provide a valid URL to test (starting with http:// or https://): ')

        if not self.username:
            self.username = input('Please provide a username to login: ')

        if not self.password:    
            self.password = input('Please provide a password to login: ')
           

        if not self.url or not self.username or not self.password:
            self.validate_input()   

    def initialize_test(self):
        """
        Initializes the test by making the first call to the JelverAPI

        Args: None

        Returns:  None
        """
        #TODO: Make the first call to the JelverAPI to initialize the test
        print('Initializing the test with the following information:')
        print(f'url: {self.url}')
        print(f'username: {self.username}')
        result = self.api.start_test(
            self.url,
            self.username,
            self.password
        )
        self.job_id = result['jobId']
        # and return the job_id and total_cases
        result = self.api.list_cases()

        self.nb_cases = len(result['testingCases'])
        self.cases_done = []

    def get_status(self):
        """
        Gets the status of the test by making the second call to the JelverAPI
        Args: None
        Returns:  status (dict): The status of the test
        """
        time.sleep(1.5)
        status = self.api.get_status(self.job_id)
        return status

    def run(self):
        """
        Runs the test
        Args: None
        Returns:  None
        """
        self.initialize_test()
        render = Render()
        render.create_progress_bar(self.job_id, self.nb_cases)

        while not self.is_completed:
            status = self.get_status()
            render.progress_bar_loading()
            cases_done = status['caseStatuses']['completed']
            cases_in_progress = status['caseStatuses']['inProgress']
            self.is_completed = status['isCompleted']

            if len(cases_in_progress) == 0:
                self.is_completed = True

            for case in cases_done:
                case_id = case['caseId']
                if case_id not in self.cases_done:
                    case_status = case_id not in \
                        [error_case['caseId'] for error_case in status['result']['caseResults']]
                    self.cases_done.append(case_id)
                    render.print_progress_bar(
                        case_id,
                        case['caseName'],
                        case_status,
                    )

        flag_success = not status['containsError']
        render.close(flag_success)
        if not flag_success:
            failed_cases = status['result']['caseErrors']
            raise JelverTestException(
                status['result']['testExceptions'],
                failed_cases,
                self.job_id
            )
