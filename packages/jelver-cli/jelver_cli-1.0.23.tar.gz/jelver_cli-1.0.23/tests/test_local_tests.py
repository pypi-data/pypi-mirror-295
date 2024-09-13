""" File to test locally running tests """

from src.local_tests import LocalTests


def test__run_tests_locally__run_successfully():
    """
    Make sure tests can run locally.
    """
    # TODO: Make function properly
    api_key = ''
    local_tests = LocalTests(
        'https://m.calipsa.biz',
        api_key
    )
    local_tests.run()
