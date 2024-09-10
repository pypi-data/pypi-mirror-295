import os
import re
from collections import namedtuple
from typing import Any
import json
import requests
import doctest

from dvttestkit import testKitUtils

logger = testKitUtils.makeLogger(__name__)


def set_status_testing(jira_domain: str = os.getenv("JiraDomain"), transition_name: str = "DVT Testing",
                       issue_key: str = os.getenv('TicketKey')):
    #     """
    #     Changes the status of the specified Jira ticket to `transition_name`.
    #
    #     :param transition_name: The target status name to set.
    #     :type transition_name: str
    #     :param issue_key: The Jira ticket key.
    #     :type issue_key: str
    #     :return: HTTP status code of the POST request.
    #     :rtype: int
    #     """
    pass


def get_test_run_info(api_token: str, email: str, test_run_id: str) -> requests.Response:
    """
    This function retrieves information about a specific test run using the QA Deputy API.

    Args:
        api_token (str): The API token for authorization.
        email (str): The email associated with the API token.
        test_run_id (str): The ID of the test run to retrieve.

    Returns:
        requests.Response: The response from the API call.

    Doctests:
        >>> class MockResponse:
        ...     @staticmethod
        ...     def json():
        ...         return {'status': 'success', 'data': {'test_run_id': '123'}}
        ...     status_code = 200

        >>> def mock_get(*args, **kwargs):
        ...     return MockResponse()

        >>> requests.get = mock_get
        >>> response = get_test_run_info('dummy_token', 'example@email.com', '123')
        >>> response.json()
        {'status': 'success', 'data': {'test_run_id': '123'}}
        >>> response.status_code
        200
    """

    headers = {
            'Authorization': api_token,
            'email':         email,
            'Content-Type':  'application/json',
            'Accept':        'application/json'
            }

    url = f'https://app.qadeputy.com/api/v1/test-run/{test_run_id}'

    return requests.get(url, headers=headers)


def get_incomplete_test_runs(api_token: str, email: str, per_page: int) -> requests.Response:
    """
    This function retrieves a paginated list of incomplete test runs using the QA Deputy API.

    Args:
        api_token (str): The API token for authorization.
        email (str): The email associated with the API token.
        per_page (int): Number of test runs to retrieve per page.

    Returns:
        requests.Response: The response from the API call.

    Doctests:
    >>> class MockResponse:
    ...     @staticmethod
    ...     def json():
    ...         return {
    ...             "data": [{"test_run_id": 201, "name": "Test Run -XX", "test_run_status": "Active", "total_test_cases_count": 3}],
    ...             "links": {"first": "http://app.qadeputy.com/api/v1/test-runs?page=1", "next": "http://app.qadeputy.com/api/v1/test-runs?page=2"},
    ...             "meta": {"current_page": 1, "per_page": "15", "total": 55}
    ...         }
    ...     status_code = 200

    >>> def mock_get(*args, **kwargs):
    ...     return MockResponse()

    >>> requests.get = mock_get
    >>> response = get_incomplete_test_runs('dummy_token', 'example@email.com', 10)
    >>> response_json = response.json()
    >>> response_json["data"][0]["test_run_id"], response_json["meta"]["total"]
    (201, 55)
    >>> response.status_code
    200
    """

    headers = {
        'Authorization': api_token,
        'email': email,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    params = {
        'is_completed': 0,
        'pagination': True,
        'per_page': per_page,
        'page': 1
    }

    url = 'https://app.qadeputy.com/api/v1/test-runs'

    return requests.get(url, headers=headers, params=params)


def create_test_run(api_token: str, email: str, name: str, description: str, test_suite_id: int, user_ids: list, test_case_ids: list) -> requests.Response:
    """
    This function creates a new test run in the QA Deputy API.

    Args:
        api_token (str): The API token for authorization.
        email (str): The email associated with the API token.
        name (str): Name of the test run.
        description (str): Description of the test run.
        test_suite_id (int): ID of the test suite.
        user_ids (list): List of user IDs.
        test_case_ids (list): List of test case IDs.

    Returns:
        requests.Response: The response from the API call.

    Doctests:
    >>> class MockResponse:
    ...     @staticmethod
    ...     def json():
    ...         return {
    ...             "test_run_id": 668,
    ...             "name": "Test Run RX10",
    ...             "description": "Lorem Ipsum is simply dummy text of the printing and typesetting industry",
    ...             "test_suite_id": 268,
    ...             "test_suite_name": "Test Suite -- RX10",
    ...             "total_test_cases_count": 2
    ...         }
    ...     status_code = 200

    >>> def mock_post(*args, **kwargs):
    ...     return MockResponse()

    >>> requests.post = mock_post
    >>> response = create_test_run('dummy_token', 'example@email.com', 'Test Run RX10', 'Lorem Ipsum...', 268, [22, 23], [101, 102])
    >>> response_json = response.json()
    >>> response_json["test_run_id"], response_json["total_test_cases_count"]
    (668, 2)
    >>> response.status_code
    200
    """

    headers = {
        'Authorization': api_token,
        'email': email,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    data = {
        'name': name,
        'description': description,
        'test_suite': test_suite_id,
        'users': user_ids,
        'include_all': False,
        'test_cases': test_case_ids
    }

    url = 'https://app.qadeputy.com/api/v1/test-runs'

    return requests.post(url, headers=headers, data=json.dumps(data))


def update_test_run(api_token: str, email: str, test_run_id: int, name: str, description: str) -> requests.Response:
    """
    This function updates an existing test run in the QA Deputy API.

    Args:
        api_token (str): The API token for authorization.
        email (str): The email associated with the API token.
        test_run_id (int): The ID of the test run to update.
        name (str): The new name for the test run.
        description (str): The new description for the test run.

    Returns:
        requests.Response: The response from the API call.

    Doctests:
    >>> class MockResponse:
    ...     @staticmethod
    ...     def json():
    ...         return {
    ...             "test_run_id": 668,
    ...             "name": "Test Run RX10 --updated",
    ...             "description": "Lorem Ipsum -- updated",
    ...             "total_test_cases_count": 3
    ...         }
    ...     status_code = 200

    >>> def mock_put(*args, **kwargs):
    ...     return MockResponse()

    >>> requests.put = mock_put
    >>> response = update_test_run('dummy_token', 'example@email.com', 668, 'Test Run RX10 --updated', 'Lorem Ipsum -- updated')
    >>> response_json = response.json()
    >>> response_json["test_run_id"], response_json["name"]
    (668, 'Test Run RX10 --updated')
    >>> response.status_code
    200
    """

    headers = {
        'Authorization': api_token,
        'email': email,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    data = {
        'name': name,
        'description': description
    }

    url = f'https://app.qadeputy.com/api/v1/test-runs/{test_run_id}'

    return requests.put(url, headers=headers, data=json.dumps(data))


def get_test_cases_for_run(api_token: str, email: str, test_run_id: int, per_page: int) -> requests.Response:
    """
    This function retrieves a list of test cases for a specific test run using the QA Deputy API.

    Args:
        api_token (str): The API token for authorization.
        email (str): The email associated with the API token.
        test_run_id (int): The ID of the test run.
        per_page (int): Number of test cases to retrieve per page.

    Returns:
        requests.Response: The response from the API call.

    Doctests:
    >>> class MockResponse:
    ...     @staticmethod
    ...     def json():
    ...         return {
    ...             "data": [{"test_case_id": 18376, "name": "Test Case 1"}, {"test_case_id": 18902, "name": "Test Case 3"}],
    ...             "meta": {"current_page": 1, "total": 4}
    ...         }
    ...     status_code = 200

    >>> def mock_get(*args, **kwargs):
    ...     return MockResponse()

    >>> requests.get = mock_get
    >>> response = get_test_cases_for_run('dummy_token', 'example@email.com', 668, 15)
    >>> response_json = response.json()
    >>> len(response_json["data"]), response_json["meta"]["total"]
    (2, 4)
    >>> response.status_code
    200
    """

    headers = {
        'Authorization': api_token,
        'email': email,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    params = {
        'pagination': True,
        'per_page': per_page,
        'page': 1
    }

    url = f'https://app.qadeputy.com/api/v1/test-runs/{test_run_id}/test-cases'

    return requests.get(url, headers=headers, params=params)


def update_test_case(api_token: str, email: str, test_run_id: int, test_case_id: int, test_case_status: int, actual_result: str) -> requests.Response:
    """
    This function updates the status and actual result of a specific test case in a test run using the QA Deputy API.

    Args:
        api_token (str): The API token for authorization.
        email (str): The email associated with the API token.
        test_run_id (int): The ID of the test run.
        test_case_id (int): The ID of the test case to update.
        test_case_status (int): The new status for the test case.
        actual_result (str): The actual result of the test case.

    Returns:
        requests.Response: The response from the API call.

    Doctests:
    >>> class MockResponse:
    ...     @staticmethod
    ...     def json():
    ...         return {
    ...             "previous_value": [{"test_case_status": 1, "actual_result": None}],
    ...             "updated_value": [{"test_case_status": 2, "actual_result": "Test actual result"}]
    ...         }
    ...     status_code = 200

    >>> def mock_put(*args, **kwargs):
    ...     return MockResponse()

    >>> requests.put = mock_put
    >>> response = update_test_case('dummy_token', 'example@email.com', 1001, 501, 2, 'Test actual result')
    >>> response_json = response.json()
    >>> response_json["updated_value"][0]["test_case_status"], response_json["updated_value"][0]["actual_result"]
    (2, 'Test actual result')
    >>> response.status_code
    200
    """

    headers = {
        'Authorization': api_token,
        'email': email,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    data = {
        'test_case_status': test_case_status,
        'actual_result': actual_result
    }

    url = f'https://app.qadeputy.com/api/v1/test-runs/{test_run_id}/test-cases/{test_case_id}'

    return requests.put(url, headers=headers, data=json.dumps(data))


def get_custom_test_case_statuses(api_token: str, email: str, per_page: int) -> requests.Response:
    """
    This function retrieves a list of custom test case statuses from the QA Deputy API.

    Args:
        api_token (str): The API token for authorization.
        email (str): The email associated with the API token.
        per_page (int): Number of test case statuses to retrieve per page.

    Returns:
        requests.Response: The response from the API call.

    Doctests:
    >>> class MockResponse:
    ...     @staticmethod
    ...     def json():
    ...         return {
    ...             "data": [{"test_case_status_id": 6, "name": "Completed"}, {"test_case_status_id": 16, "name": "Reset Mode"}],
    ...             "meta": {"current_page": 1, "total": 7}
    ...         }
    ...     status_code = 200

    >>> def mock_get(*args, **kwargs):
    ...     return MockResponse()

    >>> requests.get = mock_get
    >>> response = get_custom_test_case_statuses('dummy_token', 'example@email.com', 15)
    >>> response_json = response.json()
    >>> len(response_json["data"]), response_json["meta"]["total"]
    (2, 7)
    >>> response.status_code
    200
    """

    headers = {
        'Authorization': api_token,
        'email': email,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    params = {
        'status_type': 'custom_status',
        'pagination': True,
        'per_page': per_page,
        'page': 1
    }

    url = 'https://app.qadeputy.com/api/v1/test-case-statuses'

    return requests.get(url, headers=headers, params=params)


def update_test_suite(api_token: str, email: str, test_suite_id: int, name: str, description: str, product_id: int) -> requests.Response:
    """
    This function updates a test suite in the QA Deputy API.

    Args:
        api_token (str): The API token for authorization.
        email (str): The email associated with the API token.
        test_suite_id (int): The ID of the test suite to update.
        name (str): The new name for the test suite.
        description (str): The new description for the test suite.
        product_id (int): The product ID associated with the test suite.

    Returns:
        requests.Response: The response from the API call.

    Doctests:
    >>> class MockResponse:
    ...     @staticmethod
    ...     def json():
    ...         return {
    ...             "test_suite_id": 268,
    ...             "name": "Test Suite -- RX10 --update",
    ...             "description": "DESC --update",
    ...             "product_id": 27
    ...         }
    ...     status_code = 200

    >>> def mock_put(*args, **kwargs):
    ...     return MockResponse()

    >>> requests.put = mock_put
    >>> response = update_test_suite('dummy_token', 'example@email.com', 268, 'Test Suite -- RX10 --update', 'DESC --update', 27)
    >>> response_json = response.json()
    >>> response_json["test_suite_id"], response_json["name"]
    (268, 'Test Suite -- RX10 --update')
    >>> response.status_code
    200
    """

    headers = {
        'Authorization': api_token,
        'email': email,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    data = {
        'name': name,
        'description': description,
        'product': product_id
    }

    url = f'https://app.qadeputy.com/api/v1/test-suites/{test_suite_id}'

    return requests.put(url, headers=headers, data=json.dumps(data))


def create_test_suite(api_token: str, email: str, name: str, description: str, product_id: int) -> requests.Response:
    """
    This function creates a new test suite in the QA Deputy API.

    Args:
        api_token (str): The API token for authorization.
        email (str): The email associated with the API token.
        name (str): Name of the test suite.
        description (str): Description of the test suite.
        product_id (int): The product ID associated with the test suite.

    Returns:
        requests.Response: The response from the API call.

    Doctests:
    >>> class MockResponse:
    ...     @staticmethod
    ...     def json():
    ...         return {
    ...             "test_suite_id": 271,
    ...             "name": "test Suite --create",
    ...             "description": "lorem Ipsum",
    ...             "product_id": 27
    ...         }
    ...     status_code = 200

    >>> def mock_post(*args, **kwargs):
    ...     return MockResponse()

    >>> requests.post = mock_post
    >>> response = create_test_suite('dummy_token', 'example@email.com', 'test Suite --create', 'lorem Ipsum', 27)
    >>> response_json = response.json()
    >>> response_json["test_suite_id"], response_json["name"]
    (271, 'test Suite --create')
    >>> response.status_code
    200
    """

    headers = {
        'Authorization': api_token,
        'email': email,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    data = {
        'name': name,
        'description': description,
        'product': product_id
    }

    url = 'https://app.qadeputy.com/api/v1/test-suites'

    return requests.post(url, headers=headers, data=json.dumps(data))


def get_test_cases_in_suite(api_token: str, email: str, test_suite_id: int, test_case_status: str, per_page: int) -> requests.Response:
    """
    This function retrieves test cases for a specific test suite from the QA Deputy API.

    Args:
        api_token (str): The API token for authorization.
        email (str): The email associated with the API token.
        test_suite_id (int): The ID of the test suite.
        test_case_status (str): The status of the test cases to filter by.
        per_page (int): Number of test cases to retrieve per page.

    Returns:
        requests.Response: The response from the API call.

    Doctests:
    >>> class MockResponse:
    ...     @staticmethod
    ...     def json():
    ...         return {
    ...             "data": [{"test_case_id": 47228, "name": "ReportingService/GetTimeOffTypeFilter"}, {"test_case_id": 47229, "name": "ReportingService/Ping"}],
    ...             "meta": {"current_page": 1, "total": 3}
    ...         }
    ...     status_code = 200

    >>> def mock_get(*args, **kwargs):
    ...     return MockResponse()

    >>> requests.get = mock_get
    >>> response = get_test_cases_in_suite('dummy_token', 'example@email.com', 268, 'active', 15)
    >>> response_json = response.json()
    >>> len(response_json["data"]), response_json["meta"]["total"]
    (2, 3)
    >>> response.status_code
    200
    """

    headers = {
        'Authorization': api_token,
        'email': email,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    params = {
        'test_case_status': test_case_status,
        'per_page': per_page,
        'page': 1
    }

    url = f'https://app.qadeputy.com/api/v1/test-suites/{test_suite_id}/test-cases'

    return requests.get(url, headers=headers, params=params)


def get_test_case_details(api_token: str, email: str, test_suite_id: int, test_case_id: int) -> requests.Response:
    """
    This function retrieves detailed information about a specific test case within a test suite from the QA Deputy API.

    Args:
        api_token (str): The API token for authorization.
        email (str): The email associated with the API token.
        test_suite_id (int): The ID of the test suite.
        test_case_id (int): The ID of the test case to retrieve details for.

    Returns:
        requests.Response: The response from the API call.

    Doctests:
    >>> class MockResponse:
    ...     @staticmethod
    ...     def json():
    ...         return {
    ...             "test_case_id": 47230,
    ...             "name": "ZenQ Test - ReportingService/GetTimeOffReport Copy",
    ...             "test_feature": "uAttend QA - Reporting API --2"
    ...         }
    ...     status_code = 200

    >>> def mock_get(*args, **kwargs):
    ...     return MockResponse()

    >>> requests.get = mock_get
    >>> response = get_test_case_details('dummy_token', 'example@email.com', 268, 47230)
    >>> response_json = response.json()
    >>> response_json["test_case_id"], response_json["name"]
    (47230, 'ZenQ Test - ReportingService/GetTimeOffReport Copy')
    >>> response.status_code
    200
    """

    headers = {
        'Authorization': api_token,
        'email': email,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    url = f'https://app.qadeputy.com/api/v1/test-suites/{test_suite_id}/test-cases/{test_case_id}'

    return requests.get(url, headers=headers)


def update_test_case_details(api_token: str, email: str, test_suite_id: int, test_case_id: int, name: str, preconditions: str, expected_results: str, test_case_steps: str, specifications: str, time: str) -> requests.Response:
    """
    This function updates details of a specific test case within a test suite using the QA Deputy API.

    Args:
        api_token (str): The API token for authorization.
        email (str): The email associated with the API token.
        test_suite_id (int): The ID of the test suite.
        test_case_id (int): The ID of the test case to update.
        name (str): Updated name of the test case.
        preconditions (str): Updated preconditions of the test case.
        expected_results (str): Updated expected results of the test case.
        test_case_steps (str): Updated test case steps.
        specifications (str): Updated specifications URL.
        time (str): Updated time value for the test case.

    Returns:
        requests.Response: The response from the API call.

    Doctests:
    >>> class MockResponse:
    ...     @staticmethod
    ...     def json():
    ...         return {
    ...             "test_case_id": 47230,
    ...             "name": "Test Case --updated",
    ...             "preconditions": "desc",
    ...             "test_case_steps": "desc",
    ...             "expected_results": "desc",
    ...             "specifications": "https://www.example.com",
    ...             "time": "23:12"
    ...         }
    ...     status_code = 200

    >>> def mock_put(*args, **kwargs):
    ...     return MockResponse()

    >>> requests.put = mock_put
    >>> response = update_test_case_details('dummy_token', 'example@email.com', 268, 47230, 'Test Case --updated', 'desc', 'desc', 'desc', 'https://www.example.com', '23:12')
    >>> response_json = response.json()
    >>> response_json["test_case_id"], response_json["name"]
    (47230, 'Test Case --updated')
    >>> response.status_code
    200
    """

    headers = {
        'Authorization': api_token,
        'email': email,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    data = {
        'name': name,
        'preconditions': preconditions,
        'expected_results': expected_results,
        'test_case_steps': test_case_steps,
        'specifications': specifications,
        'time': time
    }

    url = f'https://app.qadeputy.com/api/v1/test-suites/{test_suite_id}/test-cases/{test_case_id}'

    return requests.put(url, headers=headers, data=json.dumps(data))


def create_test_case(api_token: str, email: str, test_suite_id: int, test_feature_id: int, name: str, preconditions: str, expected_results: str, test_case_steps: str, specifications: str, time: str) -> requests.Response:
    """
    This function creates a new test case in a specific test suite using the QA Deputy API.

    Args:
        api_token (str): The API token for authorization.
        email (str): The email associated with the API token.
        test_suite_id (int): The ID of the test suite.
        test_feature_id (int): The ID of the test feature.
        name (str): Name of the test case.
        preconditions (str): Preconditions of the test case.
        expected_results (str): Expected results of the test case.
        test_case_steps (str): Test case steps.
        specifications (str): Specifications URL.
        time (str): Time value for the test case.

    Returns:
        requests.Response: The response from the API call.

    Doctests:
    >>> class MockResponse:
    ...     @staticmethod
    ...     def json():
    ...         return {
    ...             "test_case_id": 48969,
    ...             "name": "Test Case create --logo A",
    ...             "preconditions": "desc",
    ...             "test_case_steps": "desc",
    ...             "expected_results": "desc",
    ...             "specifications": "https://www.example.com",
    ...             "time": "23:12"
    ...         }
    ...     status_code = 200

    >>> def mock_post(*args, **kwargs):
    ...     return MockResponse()

    >>> requests.post = mock_post
    >>> response = create_test_case('dummy_token', 'example@email.com', 268, 5395, 'Test Case create --logo A', 'desc', 'desc', 'desc', 'https://www.example.com', '23:12')
    >>> response_json = response.json()
    >>> response_json["test_case_id"], response_json["name"]
    (48969, 'Test Case create --logo A')
    >>> response.status_code
    200
    """

    headers = {
        'Authorization': api_token,
        'email': email,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    data = {
        'test_feature_id': test_feature_id,
        'name': name,
        'preconditions': preconditions,
        'expected_results': expected_results,
        'test_case_steps': test_case_steps,
        'specifications': specifications,
        'time': time
    }

    url = f'https://app.qadeputy.com/api/v1/test-suites/{test_suite_id}/test-cases'

    return requests.post(url, headers=headers, data=json.dumps(data))


def add_test_case_result(api_token: str, email: str, test_case_id: int, test_case_status: int, actual_result: str, created_by_user_id: int, test_run_id: int) -> requests.Response:
    """
    This function adds a test result to a specific test case using the QA Deputy API.

    Args:
        api_token (str): The API token for authorization.
        email (str): The email associated with the API token.
        test_case_id (int): The ID of the test case.
        test_case_status (int): The status ID of the test case result.
        actual_result (str): The actual result of the test case.
        created_by_user_id (int): The user ID of the person who created the test result.
        test_run_id (int): The ID of the test run associated with the test case.

    Returns:
        requests.Response: The response from the API call.

    Doctests:
    >>> class MockResponse:
    ...     @staticmethod
    ...     def json():
    ...         return {
    ...             "test_case_id": "47230",
    ...             "test_case_name": "Test Case --updated",
    ...             "test_case_status": "Passed",
    ...             "actual_result": "test result is Passed",
    ...             "created_by": "Admin George"
    ...         }
    ...     status_code = 200

    >>> def mock_post(*args, **kwargs):
    ...     return MockResponse()

    >>> requests.post = mock_post
    >>> response = add_test_case_result('dummy_token', 'example@email.com', 47230, 3, 'test result is Passed', 74, 754)
    >>> response_json = response.json()
    >>> response_json["test_case_id"], response_json["actual_result"]
    ('47230', 'test result is Passed')
    >>> response.status_code
    200
    """

    headers = {
        'Authorization': api_token,
        'email': email,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    data = {
        'test_case_status': test_case_status,
        'actual_result': actual_result,
        'created_by_user_id': created_by_user_id,
        'test_run': test_run_id
    }

    url = f'https://app.qadeputy.com/api/v1/test-cases/{test_case_id}/test-results'

    return requests.post(url, headers=headers, data=json.dumps(data))


def get_test_case_results(api_token: str, email: str, test_case_id: int, per_page: int, current_page: int) -> requests.Response:
    """
    This function retrieves test results for a specific test case from the QA Deputy API.

    Args:
        api_token (str): The API token for authorization.
        email (str): The email associated with the API token.
        test_case_id (int): The ID of the test case.
        per_page (int): Number of results per page.
        current_page (int): The current page number for pagination.

    Returns:
        requests.Response: The response from the API call.

    Doctests:
    >>> class MockResponse:
    ...     @staticmethod
    ...     def json():
    ...         return {
    ...             "data": [{"test_case_id": 47230, "test_case_name": "Test Case --updated --new", "test_case_status": "Failed"}],
    ...             "meta": {"current_page": 1, "total": 27}
    ...         }
    ...     status_code = 200

    >>> def mock_get(*args, **kwargs):
    ...     return MockResponse()

    >>> requests.get = mock_get
    >>> response = get_test_case_results('dummy_token', 'example@email.com', 47230, 15, 1)
    >>> response_json = response.json()
    >>> len(response_json["data"]), response_json["meta"]["total"]
    (1, 27)
    >>> response.status_code
    200
    """

    headers = {
        'Authorization': api_token,
        'email': email,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    params = {
        'pagination': True,
        'per_page': per_page,
        'page': current_page
    }

    url = f'https://app.qadeputy.com/api/v1/test-cases/{test_case_id}/test-results'

    return requests.get(url, headers=headers, params=params)



# Example usage
# response = get_test_run_info('your_api_token', 'your_email', 'test_run_id_1')
# print(response.json())


if __name__ == '__main__':
    # You can now call this function like so:
    # response = update_test_status("your_api_token", "your_test_execution_id", "EXECUTING")
    doctest.testmod()
