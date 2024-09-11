"""Handles the API calls for the notification policy."""

from typing import Dict

from spyctl.api.primitives import get, post, put


def get_notification_policy(api_url, api_key, org_uid) -> Dict:
    """
    Retrieves the notification policy for a given organization.

    Args:
        api_url (str): The base URL of the API.
        api_key (str): The API key for authentication.
        org_uid (str): The unique identifier of the organization.

    Returns:
        dict: The notification policy as a dictionary.

    """
    url = f"{api_url}/api/v1/org/{org_uid}/notification_policy/"
    json = get(url, api_key).json()
    return json


def put_notification_policy(api_url, api_key, org_uid, notification_pol):
    """
    Updates the notification policy for a given organization.

    Args:
        api_url (str): The base URL of the API.
        api_key (str): The API key for authentication.
        org_uid (str): The unique identifier of the organization.
        notification_pol (dict): The updated notification policy.

    Returns:
        dict: The response from the API.

    """
    url = f"{api_url}/api/v1/org/{org_uid}/notification_policy/"
    resp = put(url, notification_pol, api_key)
    return resp


def post_test_notification(api_url, api_key, org_uid, target_name):
    """
    Sends a test notification to a target.

    Args:
        api_url (str): The URL of the API.
        api_key (str): The API key for authentication.
        org_uid (str): The unique identifier of the organization.
        target_name (str): The name of the target to send the notification to.

    Returns:
        dict: The response from the API.

    """
    url = f"{api_url}/api/v1/org/{org_uid}/notification_policy/test_target"
    resp = post(url, {"target": target_name}, api_key)
    return resp
