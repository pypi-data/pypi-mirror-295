import config
from colorama import Fore, Style

class JelverBaseException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        return Fore.RED + Style.BRIGHT + \
           f'\n\nJelverBaseException: {self.message}' + \
           Style.RESET_ALL


class JelverAPIException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        return Fore.RED + Style.BRIGHT + \
           f'\n\nJelverAPIException: {self.message}' + \
           Style.RESET_ALL + \
           '\n\n' + \
           Style.DIM + \
           'Please provide a valid API Key to run the tests\n\n' + \
           Style.RESET_ALL + \
           Fore.BLUE + \
           '\tjelver test --api-key=YOUR_API_KEY'+ \
           Style.RESET_ALL + \
           Style.DIM + \
           '\n\nIf you don\'t have an API_KEY, please go here: \n' + \
           Style.RESET_ALL + \
           Fore.CYAN + \
           f'{config.APP_HOST}/integration\n' + \
           Style.RESET_ALL 


class JelverCasesException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        return Fore.RED + Style.BRIGHT + \
           f'\n\nJelverCASESException: {self.message}' + \
           Style.RESET_ALL + \
           '\n\n' + \
           Style.DIM + \
           'Please check which cases you have here:\n\n' + \
           Style.RESET_ALL + \
           Fore.BLUE + \
           '\tjelver cases ls --api-key=YOUR_API_KEY'+ \
           Style.RESET_ALL


class JelverTestException(Exception):
    """
    Class to throw an exception when tests fail.
    """
    def __init__(self, message, failed_cases, job_id):
        self.message = message
        self.failed_cases = failed_cases
        self.job_id = job_id
        super().__init__(self.message)

    def __str__(self):
        message = ''
        if self.message:
            message += f'{self.message}\n\n'

        if len(self.failed_cases):
            message += (
                f"Number of failed tests {len(self.failed_cases)}. " +
                "Please check the logs for more information"
            )

        message_error = Fore.RED + Style.BRIGHT + \
           f'\n\nJelverTestException: {self.message}' + \
           Style.RESET_ALL

        for case in self.failed_cases:
            case_id = case['caseId']
            case_name = case['caseName']
            case_error = '\n'.join(list(case['errors']))
            message_error += '\n\n' + \
               Style.DIM + \
               f'Case ID: {case_id}\n' + \
               f'Case Name: {case_name}' + \
               '\n\nThis is what we have seen:\n'+ \
               Style.RESET_ALL + \
               Fore.CYAN + \
               case_error + \
               Style.RESET_ALL

        message_error += (
            '\n\nTo see an overview of the test go to:\n' +
            Style.RESET_ALL + \
            Fore.CYAN + \
            f'{config.APP_HOST}/report/?jobId={self.job_id}\n' +
            Style.RESET_ALL
        )
        return  message_error
