import json
import os
import re
import warnings
from collections import namedtuple
from typing import Any
from typing import List
from typing import Optional

from atlassian import Jira
from urllib3.exceptions import NotOpenSSLWarning

warnings.filterwarnings("ignore", category=NotOpenSSLWarning)

# Setup logger
from dvttestkit import testKitUtils

logger = testKitUtils.makeLogger(__name__)

# Initialize Jira connection
jira = Jira(
    url=os.getenv("JiraDomain"),
    username=os.getenv("JiraEmail"),
    password=os.getenv("JiraToken"),
    api_version="2"
)


def get_ticket_components(issue_key: str = os.getenv('DVT_TICKET')) -> Optional[str]:
    """
    Retrieve the name of the components field for a given Jira ticket.

    :param issue_key: Jira ticket key (e.g. "AUTO-770")
    :return: name of the components field, or None if the request failed
    """
    try:
        issue = jira.get_issue(issue_key, fields="components")
        return issue['fields']['components']
    except Exception as e:
        logger.error(f"Failed to retrieve components for ticket {issue_key}: {e}")
        return None


def convert(dictionary: dict) -> Any:
    """
    Convert a dictionary to a namedtuple.

    :param dictionary: input dictionary
    :return: namedtuple with keys and values from the input dictionary
    """
    for key, value in dictionary.items():
        if isinstance(value, dict):
            dictionary[key] = convert(value)
    return namedtuple('GenericDict', dictionary.keys())(**dictionary)


def custom_decoder(obj: dict) -> Any:
    """
    Convert a dictionary to a namedtuple, replacing invalid characters in keys.

    :param obj: input dictionary
    :return: namedtuple with keys and values from the input dictionary, with invalid characters in keys replaced
    """

    def replace_invalid_chars(string: str) -> str:
        return re.sub(r'\W', '_', string)

    valid_keys = [replace_invalid_chars(key) for key in obj.keys()]
    return namedtuple('X', valid_keys)(*obj.values())


def update_test_status(test_execution_id: str, status: str) -> bool:
    """
    This function updates the test execution status using the Xray REST API.

    Args:
        test_execution_id (str): The id of the test execution to update.
        status (str): The new status to set for the test execution.

    Returns:
        bool: True if the update was successful, False otherwise.
    """
    url = f'https://minimco.atlassian.net/rest/raven/1.0/api/testrun/{test_execution_id}/status'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {os.getenv("JiraToken")}'
    }
    payload = {
        'status': status
    }

    response = jira.session.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        return True
    else:
        logger.error(f"Failed to update test status: {response.text}")
        return False


def get_ticket_summary(ticket_id: str, fields: str = "*all") -> List[dict]:
    """
    List all tickets on a given Jira board.

    :param fields: The fields to include in the response
    :param ticket_id: The ID of the Jira board
    :return: A list of dictionaries containing ticket information
    """
    try:
        return jira.get_issue(ticket_id, fields=fields)
    except Exception as e:
        logger.error(f"Failed to get ticket summary {ticket_id}: {e}")
        return []


def attach_file_to_ticket(issue_key: str, file_path: str) -> bool:
    """
    Attach a file to a Jira ticket.

    :param issue_key: The key of the Jira ticket (e.g., "PROJECT-123")
    :param file_path: The path to the file to attach
    :return: True if the file was successfully attached, False otherwise
    """
    try:
        # with open(file_path, 'rb') as file:
        response = jira.add_attachment(issue_key, file_path)
        if response[0]['self']:
            logger.info(f"File {file_path} successfully attached to ticket {issue_key}.")
            return True
        else:
            logger.error(f"Failed to attach file to ticket {issue_key}: {response.text}")
            return False
    except Exception as e:
        logger.error(f"Error attaching file to ticket {issue_key}: {e}")
        return False


# response = jira.get_issue_changelog(issue_key)
def list_tickets_assigned_to_user(email_address: str = os.getenv("JiraEmail"),
                                  board_id: str = os.getenv("JiraDefaultBoard")) -> List[dict]:
    """
    List all tickets assigned to a specific user by their email address.

    :param board_id:
    :param email_address: The email address of the user (e.g., "d.edens@elementalmachines.com")
    :return: A list of dictionaries containing ticket information
    """
    jql_query = f"assignee = \"{email_address}\" AND project = \"{board_id}\" ORDER BY created DESC"

    results = []
    try:
        issues = jira.jql(jql_query)
        for each in issues['issues']:
            if each.get('fields', {}).get('project', {}).get('key') == board_id:
                print(f"{each['key']}=:={each['fields']['summary']}")
                results.append(each)
        return results
    except Exception as e:
        logger.error(f"Failed to list tickets assigned to user {email_address}: {e}")
        return []


def attach_comment_to_ticket(issue_key: str, comment: str) -> bool:
    """
    Attach a comment to a Jira ticket.

    :param issue_key: The key of the Jira ticket (e.g., "PROJECT-123")
    :param comment: The comment to attach
    :return: True if the comment was successfully attached, False otherwise
    """
    try:
        response = jira.issue_add_comment(issue_key, comment)
        print(response)
        if response:
            logger.info(f"Comment successfully added to ticket {issue_key}.")
            return True
        else:
            logger.error(f"Failed to add comment to ticket {issue_key}: {response.text}")
            return False
    except Exception as e:
        logger.error(f"Error adding comment to ticket {issue_key}: {e}")
        return False


if __name__ == '__main__':

    # tickets = list_tickets_assigned_to_user_on_board(email_address, board_id="DVD")
    tickets = list_tickets_assigned_to_user()

    # print(attach_comment_to_ticket("DVD-73", "post.py"))
    # print(list_tickets_assigned_to_user("dan edens"))
    # print(get_ticket_summary(ticket_id="ES-460"))
    # print(get_ticket_components(issue_key="DVD-73"))
