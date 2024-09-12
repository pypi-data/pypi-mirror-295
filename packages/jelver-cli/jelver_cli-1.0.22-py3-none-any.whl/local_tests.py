""" File to allow running tests locally """

import os
import asyncio
import shutil
from uuid import uuid4
from pathlib import Path

from enums import CaseType
from utils.api import Api
from utils.render import Render
from utils.jelver_exceptions import JelverTestException
from utils.playwright_utils import (
    create_context_and_page,
    fetch_html_and_screenshots,
    goto_url_with_timeout
)


class LocalTests:
    """
    Class to run tests locally
    """
    def __init__(self,
            url,
            api_key,
            persistent=False,
            update_status_function=None,
            playwright_page=None,
            host_url=None,
            force_login=False,     
            using_cli=False):
        """ Initialize the LocalTests class """
        # pylint: disable=too-many-arguments
        self.api = Api(
            api_key,
            host_url=host_url
        )
        self.url = url
        self.force_login = force_login     
        self.update_status_function=update_status_function
        self.page = playwright_page
        self.using_cli = using_cli
        self.context = None
        self.profile_dir = Path("./.jelver_browser_profiles/")

    def run(self):
        """Run the workflow synchronously"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.login_check())
        return loop.run_until_complete(self.run_tests_locally())

    async def login_check(self):
        """Check if the user is logged in"""
        try:
            if self.force_login and \
                self.using_cli and \
                os.path.exists(self.profile_dir):
                shutil.rmtree(self.profile_dir)
            # Step 1: Check if the profile exists, create a persistent context if it doesn't
            if not self.profile_dir.exists():
                input("\nA new window will open, please login to the page for us to run the tests.\nPress Enter to continue...")
                self.context, page = await create_context_and_page(
                    profile_dir=self.profile_dir,
                    headless=False,  # Disable headless mode for login
                    persistent=True  # Create a persistent context to save the session
                )
                await page.goto(self.url, wait_until='domcontentloaded')
                input("Press Enter once you've logged in...")
                self.profile_dir.mkdir(parents=True, exist_ok=True)
        finally:    
           if self.context:
                await self.context.close()

    async def run_tests_locally(self):
        """
        Run the E2E test workflow 
        """
        # pylint: disable=too-many-arguments
        job_id = str(uuid4())

        try:
            if self.page is None:
                self.context, self.page = await create_context_and_page(
                    profile_dir=self.profile_dir,
                    persistent=True,
                    headless=True
                )
            return await self.run_algorithm(job_id)

        finally:
            if self.context:
                await self.context.close()

    async def run_algorithm(self, job_id):
        # pylint: disable=too-many-arguments, too-many-locals
        """
        Run the overall testing algorithm.
        """
        render = Render()
        cases = self.api.list_cases()
        

        testing_cases = cases['testingCases']
        render.create_progress_bar(job_id, len(testing_cases))
        

        for case in testing_cases:
            case_id, case_info, case_type = self.extract_case_details(case)

            if case_type != CaseType.ROUTE.value:
                raise ValueError(f'Invalid Case Type of ID "{case_id}" Type "{case_type}"')

            page_url = f'{self.url.rstrip("/")}/{case_info.lstrip("/")}'
            self.page = await goto_url_with_timeout(self.page, page_url)
            html, screenshots = await fetch_html_and_screenshots(self.page)
            status = self.api.test_case(job_id, case_id, html, screenshots)
            case_status = case_id not in \
                [error['caseId'] for error in status['result']['caseErrors']]
            render.print_progress_bar(
                case_id,
                case['caseName'],
                case_status,
            )

            if self.update_status_function:
                self.update_status_function(status)

        flag_success = not status['containsError']
        render.close(flag_success)
        # Only raise an exception when using the CLI
        if not flag_success and self.using_cli:
            failed_cases = status['result']['caseErrors']
            raise JelverTestException(
                status['result']['testExceptions'],
                failed_cases,
                job_id
            )
        return status


    def extract_case_details(self, case):
        """
        Extract case details from the provided case
        """
        return case['caseId'], case['caseInfo'], case['caseType']
