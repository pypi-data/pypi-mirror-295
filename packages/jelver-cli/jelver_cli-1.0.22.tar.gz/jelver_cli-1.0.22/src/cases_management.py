from colorama import Fore, Style
from tabulate import tabulate

from utils.api import Api

class CasesManagement:
    def __init__(self, api_key):
        self.include_cases = []
        self.exclude_cases = []
        self.api = Api(api_key)

    def add(self, case_ids):    
        """
        Include the cases that you want to test

        Arguments:
        :case_ids: list: The case ids that you want to include

        Return: None
        """
        print("Including the cases...")
        self.api.add_case(case_ids.split(','))
        print(Fore.BLUE + \
            f"The cases {case_ids} have been included successfully" \
            + Style.RESET_ALL)

    def remove(self, case_ids):    
        """
        Exclude the cases that you don't want to test

        Arguments:
        :case_ids: list: The case ids that you want to exclude

        Return: None
        """
        print("Excluding the cases...")
        self.api.remove_case(case_ids.split(','))
        print(Fore.BLUE + \
            f"The cases {case_ids} have been excluded successfully" \
            + Style.RESET_ALL)

    def list(self):
        """
        List all the cases that are recorded from your application

        Return: None
        """
        print("Reaching out to the server...")
        result = self.api.list_cases()
        self.include_cases = result["testingCases"]
        self.exclude_cases = result["excludedCases"]

        include_table = [[
            Fore.BLUE + Style.BRIGHT + "Case ID" + Style.RESET_ALL,
            Fore.BLUE + Style.BRIGHT + "Origin" + Style.RESET_ALL,
            Fore.BLUE + Style.BRIGHT + "Case Name" + Style.RESET_ALL
        ]]
        include_table.extend([
            [case["caseId"], case["origin"], f'Testing the route {case["caseName"]}'] \
                 for case in self.include_cases])
        
        exclude_table = [[
            Fore.BLUE + Style.BRIGHT + "Case ID" + Style.RESET_ALL,
            Fore.BLUE + Style.BRIGHT + "Origin" + Style.RESET_ALL,
            Fore.BLUE + Style.BRIGHT + "Case Name" + Style.RESET_ALL
        ]]
        exclude_table.extend([
            [case["caseId"], case["origin"], f'Testing the route {case["caseName"]}'] \
                 for case in self.exclude_cases])
        print(Fore.GREEN + "\nIncluded cases" + Style.RESET_ALL)
        print(tabulate(
            include_table,
            headers="firstrow",
            tablefmt="fancy_grid")
        )
        print(Fore.RED + "Excluded cases" + Style.RESET_ALL)
        print(tabulate(
            exclude_table,
            headers="firstrow",
            tablefmt="fancy_grid")
        )



